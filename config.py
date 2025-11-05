"""
Inert Downloader Bot - Configuration
Developer: @TheInertGuy
Updates: @Theinertbotz
Support: @Theinertbotzchart

⚠️ DO NOT REMOVE CREDITS ⚠️
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # Repl URL for web downloads
    REPL_SLUG = os.getenv('REPL_SLUG', '')
    REPL_OWNER = os.getenv('REPL_OWNER', '')

    MONGO_URI = os.getenv("MONGO_URI", "")

    STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID", "-1003292407667"))

    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "7570083413").split(",") if x.strip()]

    FREE_DOWNLOAD_LIMIT = int(os.getenv("FREE_DOWNLOAD_LIMIT", "2"))

    FREE_MAX_SIZE_MB = int(os.getenv("FREE_MAX_SIZE_MB", "100"))
    PREMIUM_MAX_SIZE_MB = int(os.getenv("PREMIUM_MAX_SIZE_MB", "2000"))

    TELEGRAM_MAX_SIZE_MB = 2000
    SPLIT_SIZE_MB = 1800

    PAYMENT_QR_IMAGE = os.getenv("PAYMENT_QR_IMAGE", "https://i.ibb.co/hFjZ6CWD/photo-2025-08-10-02-24-51-7536777335068950548.jpg")

    PREMIUM_PLANS = {
        "1_month": {"days": 30, "price": "₹60"},
        "3_months": {"days": 90, "price": "₹150"},
        "6_months": {"days": 180, "price": "₹300"},
        "1_year": {"days": 365, "price": "₹500"}
    }

    DOWNLOAD_DIR = "downloads"

    # YouTube Cookies Configuration
    USE_COOKIES = os.getenv("USE_COOKIES", "True").lower() in ("true", "1", "yes")
    COOKIES_PATH = os.getenv("COOKIES_PATH", "cookies.txt")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)