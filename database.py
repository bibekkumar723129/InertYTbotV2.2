"""
Inert Downloader Bot - Database Module
Developer: @TheInertGuy
Updates: @Theinertbotz
Support: @Theinertbotzchart
"""

import asyncio
from datetime import datetime, timedelta
import sqlite3
import json
from typing import Optional, Dict, Any, Union
from config import Config

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGO_AVAILABLE = True
except ImportError:
    MongoClient = None
    ConnectionFailure = Exception
    ServerSelectionTimeoutError = Exception
    MONGO_AVAILABLE = False

class Database:
    def __init__(self):
        self.db_type = None
        self.db = None
        self.connection = None
        self._initialize_db()

    def _initialize_db(self):
        if MONGO_AVAILABLE and Config.MONGO_URI:
            try:
                self.connection = MongoClient(
                    Config.MONGO_URI,
                    serverSelectionTimeoutMS=5000
                )
                self.connection.admin.command('ping')
                self.db = self.connection['inert_downloader']
                self.users = self.db['users']
                self.db_type = "mongodb"
                print("✅ Connected to MongoDB")
            except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
                print(f"⚠️ MongoDB connection failed: {e}")
                print("📂 Falling back to SQLite...")
                self._init_sqlite()
        else:
            self._init_sqlite()

    def _init_sqlite(self):
        self.db_type = "sqlite"
        self.connection = sqlite3.connect('inert_bot.db', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                is_premium INTEGER DEFAULT 0,
                premium_expires TEXT,
                downloads_today INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                last_download_date TEXT,
                joined_date TEXT
            )
        ''')

        self.connection.commit()
        print("✅ Connected to SQLite")

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        if self.db_type == "mongodb":
            user = self.users.find_one({"user_id": user_id})
            return user
        else:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def create_user(self, user_id: int, username: Optional[str] = None, first_name: Optional[str] = None):
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "is_premium": False,
            "premium_expires": None,
            "downloads_today": 0,
            "total_downloads": 0,
            "last_download_date": None,
            "joined_date": datetime.now().isoformat()
        }

        if self.db_type == "mongodb":
            self.users.insert_one(user_data)
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, is_premium, 
                                 premium_expires, downloads_today, total_downloads,
                                 last_download_date, joined_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, 0, None, 0, 0, None, 
                  user_data['joined_date']))
            self.connection.commit()

    async def update_user(self, user_id: int, data: Dict[str, Any]):
        if self.db_type == "mongodb":
            self.users.update_one(
                {"user_id": user_id},
                {"$set": data}
            )
        else:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values()) + [user_id]
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
            self.connection.commit()

    async def is_premium(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False

        if user.get('is_premium'):
            expires = user.get('premium_expires')
            if expires:
                if self.db_type == "mongodb":
                    if isinstance(expires, str):
                        expires = datetime.fromisoformat(expires)
                else:
                    if isinstance(expires, str):
                        expires = datetime.fromisoformat(expires)

                if isinstance(expires, datetime) and expires > datetime.now():
                    return True
                else:
                    await self.update_user(user_id, {"is_premium": 0 if self.db_type == "sqlite" else False})
                    return False

        return False

    async def add_premium(self, user_id: int, days: int):
        user = await self.get_user(user_id)

        now = datetime.now()
        if user and user.get('is_premium') and user.get('premium_expires'):
            current_expires = user.get('premium_expires')
            if isinstance(current_expires, str):
                current_expires = datetime.fromisoformat(current_expires)

            if current_expires > now:
                expires = current_expires + timedelta(days=days)
            else:
                expires = now + timedelta(days=days)
        else:
            expires = now + timedelta(days=days)

        await self.update_user(user_id, {
            "is_premium": 1 if self.db_type == "sqlite" else True,
            "premium_expires": expires.isoformat()
        })

    async def check_download_limit(self, user_id: int) -> bool:
        if await self.is_premium(user_id):
            return True

        user = await self.get_user(user_id)
        if not user:
            return False

        today = datetime.now().date().isoformat()
        last_download = user.get('last_download_date')

        if last_download != today:
            await self.update_user(user_id, {
                "downloads_today": 0,
                "last_download_date": today
            })
            return True

        downloads_today = user.get('downloads_today', 0)
        return downloads_today < Config.FREE_DOWNLOAD_LIMIT

    async def increment_downloads(self, user_id: int):
        user = await self.get_user(user_id)
        today = datetime.now().date().isoformat()

        new_downloads_today = 1
        if user.get('last_download_date') == today:
            new_downloads_today = user.get('downloads_today', 0) + 1

        await self.update_user(user_id, {
            "downloads_today": new_downloads_today,
            "total_downloads": user.get('total_downloads', 0) + 1,
            "last_download_date": today
        })

    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        user = await self.get_user(user_id)
        if not user:
            return {}

        is_premium = await self.is_premium(user_id)
        stats = {
            "is_premium": is_premium,
            "total_downloads": user.get('total_downloads', 0),
            "downloads_today": user.get('downloads_today', 0),
            "downloads_remaining": "∞" if is_premium else Config.FREE_DOWNLOAD_LIMIT - user.get('downloads_today', 0)
        }

        if is_premium:
            expires = user.get('premium_expires')
            if isinstance(expires, str):
                expires = datetime.fromisoformat(expires)
            stats['premium_expires'] = expires.strftime("%Y-%m-%d")

        return stats

db = Database()