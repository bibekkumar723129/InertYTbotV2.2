# Inert Downloader Bot

An advanced, full-featured Telegram bot for downloading YouTube videos and audio with premium features.

## Overview

Inert Downloader Bot is a powerful Telegram bot built with Pyrogram v2, yt-dlp, and a hybrid database system (MongoDB/SQLite). It provides users with the ability to download YouTube videos in multiple qualities and extract audio, with a premium membership system for enhanced features.

## Recent Changes

- **2025-11-05**: YouTube Cookies Authentication System
  - Added YouTube cookies support to bypass "Sign in to confirm you're not a bot" errors
  - Implemented automatic cookies detection with fallback behavior
  - Added USE_COOKIES and COOKIES_PATH environment configuration
  - Created comprehensive COOKIES_SETUP.md guide
  - Updated downloader.py with _get_base_ydl_opts() method for cookies integration
  - Works with both video and audio downloads
  - Compatible with Render's ephemeral filesystem
  - Added security best practices to .gitignore for cookies.txt
  - Updated README.md with cookies setup instructions
  - Maintains full compatibility with premium system and progress tracking

- **2025-11-05**: Replit Environment Setup
  - Successfully configured for Replit environment
  - Installed all Python dependencies via packager tool
  - Created missing keep_alive.py for 24/7 operation support
  - Added .gitignore for Python project best practices
  - Set up workflow to run bot with web preview on port 5000
  - Configured Telegram API credentials via Replit Secrets
  - Verified bot startup with SQLite database fallback
  - Both keep-alive server (port 8080) and web preview (port 5000) running successfully

- **2025-11-05**: 24/7 Uptime & Multi-Platform Support
  - Added keep-alive server with health check endpoints for UptimeRobot
  - Implemented automatic platform detection (Replit, Render, Koyeb, Railway, Heroku, Fly.io)
  - Enhanced web download URLs to work across all hosting platforms
  - Created comprehensive UptimeRobot setup documentation
  - Updated main.py to integrate keep-alive functionality
  - Fixed Railway URL handling bug (fully-qualified URL support)

- **2025-11-04**: Initial project setup
  - Created bot with Pyrogram v2 framework
  - Implemented hybrid database system (MongoDB with SQLite fallback)
  - Added YouTube downloader with quality selection
  - Implemented premium user management system
  - Added storage channel integration for file backup
  - Created interactive quality selector with inline buttons

## Project Architecture

### Core Components

1. **main.py** - Main entry point (NEW)
   - Initializes bot with keep-alive server
   - Integrates 24/7 uptime functionality
   - Displays startup information and public URLs
   - Recommended entry point for running the bot

2. **keep_alive.py** - Health check server (NEW)
   - Flask web server with health check endpoints (/, /health, /ping)
   - Automatic platform detection for Replit, Render, Koyeb, Railway, Heroku, Fly.io
   - Public URL generation for UptimeRobot setup
   - Runs in background thread alongside bot

3. **bot.py** - Main bot application
   - Command handlers (/start, /download, /help, /premium, /stats, /add_premium)
   - YouTube link detection and processing
   - Interactive quality selection with callbacks
   - Download progress tracking
   - File upload and storage channel backup

4. **database.py** - Hybrid database system
   - MongoDB primary with auto-fallback to SQLite
   - User management with premium status tracking
   - Download limit enforcement
   - Daily reset for free users
   - Premium expiration handling

5. **downloader.py** - YouTube download module
   - Video info extraction using yt-dlp
   - Available format detection (144p - 1080p)
   - Audio-only extraction
   - Async download handling with progress callbacks

6. **web_preview.py** - Web download server (ENHANCED)
   - Flask server for direct file downloads
   - Multi-platform URL detection and generation
   - Secure download token system
   - Supports all major hosting platforms

7. **config.py** - Configuration management
   - Environment variable loading
   - API credentials
   - Download limits and file size restrictions
   - Premium plan definitions

8. **utils.py** - Utility functions
   - File size formatting
   - Duration formatting
   - Progress text generation
   - File cleanup helpers

### Features

#### Free Users
- 2 downloads per day (configurable)
- Max file size: 100MB
- Standard quality options
- Daily limit reset

#### Premium Users
- ∞ Unlimited downloads
- Max file size: 500MB
- File rename capability
- Link preview with thumbnail
- Priority downloads
- Extended quality options

### Database Schema

**Users Collection/Table:**
- user_id: Unique Telegram user ID
- username: Telegram username
- first_name: User's first name
- is_premium: Premium status boolean
- premium_expires: Premium expiration date
- downloads_today: Current day download count
- total_downloads: Lifetime download count
- last_download_date: Last download date for limit reset
- joined_date: Registration date

### Environment Configuration

Required variables in `.env`:
- API_ID: Telegram API ID
- API_HASH: Telegram API Hash
- BOT_TOKEN: Telegram Bot Token
- MONGO_URI: MongoDB connection URI (optional)
- STORAGE_CHANNEL_ID: Channel ID for file backup
- ADMIN_IDS: Comma-separated admin user IDs
- FREE_DOWNLOAD_LIMIT: Daily download limit for free users
- FREE_MAX_SIZE_MB: Max file size for free users
- PREMIUM_MAX_SIZE_MB: Max file size for premium users
- PAYMENT_QR_IMAGE: Payment QR code image URL
- USE_COOKIES: Enable YouTube cookies authentication (True/False)
- COOKIES_PATH: Path to cookies.txt file (default: cookies.txt)

### YouTube Cookies Setup

To fix "Sign in to confirm you're not a bot" errors:

1. Export cookies from your browser using [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Upload cookies.txt to the root directory
3. Set USE_COOKIES=True in environment
4. Restart the bot

See [COOKIES_SETUP.md](COOKIES_SETUP.md) for detailed instructions.

### Dependencies

- pyrogram v2.0.106 - Telegram bot framework
- tgcrypto v1.2.5 - Cryptography for Pyrogram
- yt-dlp - YouTube/media downloader
- pymongo - MongoDB driver
- python-dotenv - Environment variable management
- aiofiles - Async file operations
- pillow - Image processing

### Hosting Compatibility

The bot is designed to work on multiple platforms with automatic detection:

**Fully Supported with 24/7 Uptime:**
- ✅ **Replit** - Auto-detects REPL_SLUG and REPL_OWNER
- ✅ **Render** - Auto-detects RENDER_SERVICE_NAME
- ✅ **Koyeb** - Auto-detects KOYEB_PUBLIC_DOMAIN
- ✅ **Railway** - Auto-detects RAILWAY_STATIC_URL/RAILWAY_PUBLIC_DOMAIN
- ✅ **Heroku** - Auto-detects HEROKU_APP_NAME
- ✅ **Fly.io** - Auto-detects FLY_APP_NAME

**Other Platforms:**
- VPS - Use with UptimeRobot for 24/7 operation
- Termux (Android) - Local development

**Features:**
- Auto-detection and fallback to SQLite ensures compatibility with environments where MongoDB is not available
- Platform-specific URL generation for web downloads
- Health check endpoints for monitoring services
- Keep-alive functionality for free hosting tiers

### 24/7 Operation

The bot includes a built-in keep-alive server that works with UptimeRobot for free 24/7 operation:

**Health Check Endpoints:**
- `/` - Simple text response: "✅ Bot is alive!"
- `/health` - JSON response with status, platform, and timestamp
- `/ping` - Minimal ping response: "pong"

**Setup:**
1. Run the bot using `python main.py`
2. Copy the public URL from console output
3. Add monitor to UptimeRobot (free account)
4. Set interval to 5 minutes

**Documentation:**
- `UPTIMEROBOT_SETUP.md` - Comprehensive setup guide for all platforms
- `QUICKSTART.md` - Quick 3-step setup guide

## User Preferences

None set yet.

## Commands

- `/start` - Initialize bot and show welcome message
- `/download` - Request download link prompt
- `/help` - Show help information
- `/stats` - View user statistics
- `/premium` - View premium plans and subscription info
- `/add_premium <user_id> <days>` - Admin command to grant premium access

## Admin Features

Admins (defined in ADMIN_IDS) can:
- Grant premium access to users using /add_premium
- Access full user statistics
- Manage premium subscriptions manually

## Storage System

All downloaded files are automatically backed up to the configured storage channel (STORAGE_CHANNEL_ID) for:
- File recovery
- Bandwidth optimization
- Long-term storage
- Analytics and tracking
