"""
╔══════════════════════════════════════════════════════════╗
║           Inert Downloader Bot - Main Entry Point       ║
║                                                          ║
║  Developer: @TheInertGuy                                 ║
║  Updates Channel: @Theinertbotz                          ║
║  Support Group: @Theinertbotzchart                       ║
║                                                          ║
║  This is the main entry point for the bot with          ║
║  keep-alive functionality for 24/7 operation.           ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from keep_alive import keep_alive
from pyrogram import Client
from config import Config
from database import db

def main():
    """Main function to start the bot with keep-alive server"""
    print("\n" + "=" * 60)
    print("🚀 Starting Inert Downloader Bot...")
    print("=" * 60)
    
    print(f"📊 Database: {db.db_type.upper() if db.db_type else 'UNKNOWN'}")
    print(f"💾 Storage Channel: {Config.STORAGE_CHANNEL_ID}")
    print(f"⚙️  Free Download Limit: {Config.FREE_DOWNLOAD_LIMIT}/day")
    print("=" * 60 + "\n")
    
    # Start keep-alive server on port 8080
    keep_alive()
    
    # Start web preview server on port 5000
    from web_preview import run_web_preview
    run_web_preview()
    print("🌐 Web preview server started on http://0.0.0.0:5000")
    
    print("\n" + "=" * 60)
    print("✅ Bot is now running!")
    print("💡 Keep this window open or use a process manager")
    print("=" * 60 + "\n")
    
    from bot import app
    app.run()

if __name__ == "__main__":
    main()
