# 🤖 Inert Downloader Bot

> **Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
> **Updates Channel:** [@Theinertbotz](https://t.me/Theinertbotz)  
> **Support Group:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

---

⚠️ **IMPORTANT:** Please don't remove credits! This bot was developed with care and effort.

---

An advanced, full-featured Telegram bot for downloading YouTube videos and audio with premium features, built with Pyrogram v2, yt-dlp, and a hybrid database system.

## ✨ Features

### Free Users
- 📥 2 downloads per day
- 📦 Max file size: 100MB
- 🎯 Multiple quality options (144p - 1080p)
- 🎵 Audio-only downloads
- 📊 Download tracking

### Premium Users
- ∞ Unlimited downloads
- 📁 Extended file size limit (2GB)
- ✏️ File rename feature
- 🔍 Link preview with thumbnails
- ⚡ Priority download queue
- 📦 Auto-split for files >2GB (split into 1.8GB parts)
- Bandwidth optimization

## 🚀 Quick Start

### 1. Get Telegram API Credentials

**API_ID and API_HASH:**
1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy your API_ID and API_HASH

**BOT_TOKEN:**
1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow instructions
3. Copy the bot token

### 2. Configure Environment Variables

Create a `.env` file or add to Replit Secrets:

```env
# Required
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Optional - MongoDB (will use SQLite if not provided)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Storage Channel (create a private channel and add your bot as admin)
STORAGE_CHANNEL_ID=-1003292407667

# Admin IDs (comma-separated)
ADMIN_IDS=123456789,987654321

# Download Limits
FREE_DOWNLOAD_LIMIT=2
FREE_MAX_SIZE_MB=100
PREMIUM_MAX_SIZE_MB=2000

# Payment QR Image URL (optional)
PAYMENT_QR_IMAGE=https://example.com/payment-qr.png
```

### 3. Run the Bot

**On Replit:**
```bash
python bot.py
```

**On VPS/Local:**
```bash
pip install -r requirements.txt
python bot.py
```

**On Render/Railway/Koyeb:**
- Deploy using the provided configuration
- Set environment variables in platform settings
- Bot will auto-start

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and show welcome message |
| `/download` | Request download link prompt |
| `/help` | Show help information |
| `/stats` | View your download statistics |
| `/premium` | View premium plans |
| `/add_premium <user_id> <days>` | Admin: Grant premium access |

## 🎯 Usage

1. Start the bot with `/start`
2. Send any YouTube link
3. Select your preferred quality
4. Wait for download and upload
5. Receive your file!

## 🏗 Project Structure

```
.
├── bot.py              # Main bot application
├── config.py           # Configuration management
├── database.py         # Hybrid database system
├── downloader.py       # yt-dlp wrapper for downloads
├── utils.py            # Utility functions
├── file_splitter.py    # File splitting for large files
├── web_preview.py      # Web preview server
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration Details

### Storage Channel Setup

1. Create a private Telegram channel
2. Add your bot as an administrator
3. Get the channel ID (starts with -100)
4. Set it in `STORAGE_CHANNEL_ID`

### Admin Setup

1. Get your Telegram user ID (use @userinfobot)
2. Add to `ADMIN_IDS` (comma-separated for multiple admins)
3. Restart the bot

### MongoDB Setup (Optional)

If you want to use MongoDB instead of SQLite:

1. Create a free cluster at https://mongodb.com/cloud/atlas
2. Get your connection URI
3. Set it in `MONGO_URI`
4. Bot will automatically use MongoDB

If MongoDB is unavailable, bot automatically falls back to SQLite.

## 🌐 Hosting Platforms

### Replit
- ✅ Supported out of the box
- Set secrets in Replit Secrets
- Bot auto-starts

### Render
- ✅ Use web service or background worker
- Set environment variables in dashboard
- Use `python bot.py` as start command

### Railway/Koyeb
- ✅ Deploy from GitHub
- Set environment variables
- Auto-deployment on commit

### VPS/Dedicated Server
- ✅ Full control
- Use systemd for auto-restart
- Perfect for production

### Termux (Android)
- ✅ SQLite fallback works perfectly
- No MongoDB required
- Lightweight and efficient

## 🛡️ Security Features

- ✅ No secrets in code
- ✅ Environment-based configuration
- ✅ Admin-only commands protection
- ✅ User-based download tracking
- ✅ Automatic file cleanup

## 📊 Database Schema

**Users Table/Collection:**
- `user_id` - Telegram user ID (primary key)
- `username` - Telegram username
- `first_name` - User's first name
- `is_premium` - Premium status
- `premium_expires` - Premium expiration date
- `downloads_today` - Daily download count
- `total_downloads` - Lifetime downloads
- `last_download_date` - Last download date
- `joined_date` - Registration date

## 🎨 Premium Plans

Configure in `config.py`:

```python
PREMIUM_PLANS = {
    "1_month": {"days": 30, "price": "$5"},
    "3_months": {"days": 90, "price": "$12"},
    "6_months": {"days": 180, "price": "$20"},
    "1_year": {"days": 365, "price": "$35"}
}
```

## 🍪 YouTube Authentication Fix (New!)

**Problem:** Some YouTube videos show error: "Sign in to confirm you're not a bot"

**Solution:** Use YouTube cookies to bypass authentication

### Quick Setup:

1. **Export YouTube cookies using browser extension:**
   - Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Visit YouTube while logged in
   - Click extension → Export cookies for youtube.com
   - Save as `cookies.txt`

2. **Add to your project:**
   - **Replit:** Upload `cookies.txt` to root directory
   - **Render:** Include in repository or use persistent disk
   - **VPS:** Upload via SCP to bot directory

3. **Configure environment variables:**
   ```env
   USE_COOKIES=True
   COOKIES_PATH=cookies.txt
   ```

4. **Restart bot** - It will automatically detect and use cookies!

📚 **See [COOKIES_SETUP.md](COOKIES_SETUP.md) for detailed instructions**

---

## 🐛 Troubleshooting

**Bot not starting:**
- Check API credentials are correct
- Ensure BOT_TOKEN is from BotFather
- Verify API_ID and API_HASH match

**Downloads failing with "Sign in to confirm you're not a bot":**
- Export fresh YouTube cookies (see 🍪 section above)
- Ensure cookies.txt is in the correct location
- Check logs for "✅ Cookies file found" message
- Re-export cookies if they're older than 30 days

**Downloads failing (other reasons):**
- Check yt-dlp is installed
- Verify URL is valid YouTube link
- Check file size limits
- Try with cookies enabled (see above)

**Database errors:**
- MongoDB: Check connection URI
- SQLite: Ensure write permissions
- Bot auto-falls back to SQLite if MongoDB fails

**Storage channel not working:**
- Ensure bot is admin in channel
- Verify channel ID is correct
- Channel must be private

## 📦 Dependencies

- **pyrogram** v2.0.106 - Telegram bot framework
- **tgcrypto** v1.2.5 - Cryptography for Pyrogram
- **yt-dlp** - YouTube downloader
- **pymongo** - MongoDB driver (optional)
- **python-dotenv** - Environment management
- **aiofiles** - Async file operations
- **flask** - Web preview server

## 🤝 Contributing

This bot is designed for personal use. Feel free to fork and customize for your needs, but please keep the developer credits intact.

## 📝 License

This project is for educational purposes. Respect YouTube's Terms of Service when using.

## ⚠️ Disclaimer

This bot is for personal use only. Please respect the developer's work by keeping credits intact.

---

## 👨‍💻 Credits

**Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
**Updates Channel:** [@Theinertbotz](https://t.me/Theinertbotz)  
**Support Group:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

**⚠️ DO NOT REMOVE CREDITS - This bot was developed with care and effort!**

---

Made with ❤️ by [@TheInertGuy](https://t.me/TheInertGuy)