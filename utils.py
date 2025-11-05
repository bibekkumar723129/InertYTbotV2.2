"""
Inert Downloader Bot - Utility Functions
Developer: @TheInertGuy
Updates: @Theinertbotz
Support: @Theinertbotzchart
"""

import os
import aiohttp
import asyncio
from datetime import datetime
from typing import Optional

def format_filesize(size_bytes: int) -> str:
    if size_bytes == 0:
        return "Unknown"

    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def format_duration(seconds: int) -> str:
    if not seconds:
        return "Unknown"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def cleanup_file(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑 Cleaned up: {filepath}")
    except Exception as e:
        print(f"Error cleaning up file: {e}")

def create_progress_bar(percentage: int, length: int = 8) -> str:
    filled = int(length * percentage / 100)
    bar = '▰' * filled + '▱' * (length - filled)
    return bar

def format_eta(seconds: int) -> str:
    if seconds < 60:
        return f"00:{seconds:02d}"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def get_download_progress_text(d: dict) -> str:
    if d['status'] == 'downloading':
        current = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent = int((current / total) * 100) if total > 0 else 0

        current_mb = current / (1024 * 1024)
        total_mb = total / (1024 * 1024)

        progress_text = f"📥 Download: {create_progress_bar(percent)} {percent}%\n\n"
        progress_text += f"💾 {int(current_mb)}MB / {int(total_mb)}MB"

        return progress_text
    elif d['status'] == 'finished':
        return "✅ Download completed! Processing..."
    return "📥 Starting download..."

async def check_file_size(filepath: str, max_size_mb: int) -> tuple[bool, int]:
    if not os.path.exists(filepath):
        return False, 0

    file_size = os.path.getsize(filepath)
    file_size_mb = file_size / (1024 * 1024)

    if file_size_mb > max_size_mb:
        return False, int(file_size_mb)

    return True, int(file_size_mb)

def escape_markdown(text: str) -> str:
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

async def download_thumbnail(url: str, save_path: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    return save_path
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
    return None