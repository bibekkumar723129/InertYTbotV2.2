
# 🚀 Deployment Guide

## ⚠️ Developer Credits
**Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
**Updates Channel:** [@Theinertbotz](https://t.me/Theinertbotz)  
**Support Group:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

**DO NOT REMOVE CREDITS** - This bot was developed with care and effort.

---

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Telegram API credentials (API_ID, API_HASH)
- ✅ Bot Token from @BotFather
- ✅ MongoDB URI (optional, SQLite fallback available)
- ✅ Storage Channel ID
- ✅ Admin user IDs

---

## 🎯 Recommended: Replit Deployments

**Replit is the easiest and recommended platform for this bot.**

### Why Replit?
- ✅ Already configured and optimized
- ✅ One-click deployment
- ✅ Auto-scaling and monitoring
- ✅ Built-in secrets management
- ✅ Free tier available

### Deploy on Replit:
1. Click the **Deploy** button in your Repl
2. Configure environment variables in Replit Secrets
3. Choose deployment type (Reserved VM recommended)
4. Click **Deploy**
5. Done! Your bot is live 24/7

---

## 🌐 Alternative Platforms

### 1️⃣ Render

**Setup:**

1. **Fork/Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd inert-downloader-bot
   ```

2. **Create New Web Service on Render**
   - Go to https://render.com
   - Click **New** → **Web Service**
   - Connect your GitHub repository

3. **Configure Build Settings**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** Free or Starter

4. **Add Environment Variables**
   Go to **Environment** section and add:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   MONGO_URI=your_mongodb_uri
   STORAGE_CHANNEL_ID=-1003292407667
   ADMIN_IDS=123456789
   FREE_DOWNLOAD_LIMIT=2
   FREE_MAX_SIZE_MB=100
   PREMIUM_MAX_SIZE_MB=2000
   PAYMENT_QR_IMAGE=your_qr_url
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy**
   - Click **Create Web Service**
   - Wait for deployment to complete

**Using render.yaml (Automated):**
```bash
# The render.yaml file is already configured
# Just connect your repo and Render will auto-configure
```

**Important Notes for Render:**
- Free tier sleeps after 15 minutes of inactivity
- Upgrade to paid plan for 24/7 uptime
- File system is ephemeral (downloads folder clears on restart)

---

### 2️⃣ Koyeb

**Setup:**

1. **Prepare Repository**
   ```bash
   git clone <your-repo-url>
   cd inert-downloader-bot
   ```

2. **Create App on Koyeb**
   - Go to https://koyeb.com
   - Click **Create App**
   - Select **GitHub** deployment method

3. **Configure Deployment**
   - **Builder:** Buildpack
   - **Build command:** `pip install -r requirements.txt`
   - **Run command:** `python bot.py`
   - **Port:** 5000
   - **Instance type:** Nano or Small

4. **Environment Variables**
   Add in **Environment variables** section:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   MONGO_URI=your_mongodb_uri
   STORAGE_CHANNEL_ID=-1003292407667
   ADMIN_IDS=123456789
   FREE_DOWNLOAD_LIMIT=2
   FREE_MAX_SIZE_MB=100
   PREMIUM_MAX_SIZE_MB=2000
   ```

5. **Deploy**
   - Click **Deploy**
   - Monitor deployment logs

**Koyeb Features:**
- ✅ Always-on with free tier
- ✅ Auto-scaling
- ✅ Global edge network
- ⚠️ Limited free tier resources

---

### 3️⃣ Termux (Android)

**Perfect for personal use on Android devices!**

**Installation:**

1. **Install Termux**
   - Download from F-Droid (recommended)
   - Or Google Play Store

2. **Update Packages**
   ```bash
   pkg update && pkg upgrade -y
   ```

3. **Install Required Packages**
   ```bash
   pkg install python -y
   pkg install git -y
   pkg install ffmpeg -y
   pkg install libjpeg-turbo -y
   ```

4. **Clone Repository**
   ```bash
   cd ~
   git clone <your-repo-url>
   cd inert-downloader-bot
   ```

5. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Create .env File**
   ```bash
   nano .env
   ```
   
   Add your credentials:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   STORAGE_CHANNEL_ID=-1003292407667
   ADMIN_IDS=123456789
   FREE_DOWNLOAD_LIMIT=2
   FREE_MAX_SIZE_MB=100
   PREMIUM_MAX_SIZE_MB=2000
   ```
   
   Save: `Ctrl+X`, then `Y`, then `Enter`

7. **Run Bot**
   ```bash
   python bot.py
   ```

**Keep Bot Running (Background):**
```bash
# Install tmux for persistent sessions
pkg install tmux -y

# Start tmux session
tmux new -s inertbot

# Run bot
python bot.py

# Detach: Press Ctrl+B, then D
# Reattach later: tmux attach -t inertbot
```

**Auto-start on Termux Boot:**
```bash
# Install Termux:Boot from F-Droid
# Create startup script
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-bot.sh
```

Add:
```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/inert-downloader-bot
python bot.py
```

Make executable:
```bash
chmod +x ~/.termux/boot/start-bot.sh
```

**Termux Benefits:**
- ✅ Free and offline-capable
- ✅ No server costs
- ✅ Full control
- ✅ SQLite works perfectly
- ⚠️ Requires phone to stay on
- ⚠️ Limited by device resources

---

## 🔧 Build Process Overview

### Dependencies Installation
```bash
pip install -r requirements.txt
```

### Required System Packages
- Python 3.11+
- ffmpeg (for media processing)
- libjpeg, libpng, zlib (for image handling)

### Build Steps
1. Install Python dependencies
2. Verify yt-dlp installation
3. Create downloads directory
4. Initialize database (SQLite or MongoDB)
5. Start Flask web server (port 5000)
6. Start Pyrogram bot client

---

## 📊 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_ID` | ✅ Yes | - | Telegram API ID |
| `API_HASH` | ✅ Yes | - | Telegram API Hash |
| `BOT_TOKEN` | ✅ Yes | - | Bot token from @BotFather |
| `MONGO_URI` | ❌ No | SQLite | MongoDB connection string |
| `STORAGE_CHANNEL_ID` | ✅ Yes | - | Channel ID for backups |
| `ADMIN_IDS` | ✅ Yes | - | Comma-separated admin IDs |
| `FREE_DOWNLOAD_LIMIT` | ❌ No | 2 | Daily downloads for free users |
| `FREE_MAX_SIZE_MB` | ❌ No | 100 | Max file size for free users |
| `PREMIUM_MAX_SIZE_MB` | ❌ No | 2000 | Max file size for premium |
| `PAYMENT_QR_IMAGE` | ❌ No | - | Payment QR code URL |
| `REPL_SLUG` | ❌ Auto | - | Replit slug (auto-set) |
| `REPL_OWNER` | ❌ Auto | - | Replit owner (auto-set) |

---

## 🐛 Troubleshooting

### Common Issues:

**Bot not starting:**
- Verify all required env variables are set
- Check API credentials are correct
- Ensure bot token is valid

**Database connection failed:**
- MongoDB: Check URI format and network access
- Bot auto-falls back to SQLite if MongoDB fails

**Downloads failing:**
- Install ffmpeg: `apt-get install ffmpeg` or `pkg install ffmpeg`
- Update yt-dlp: `pip install -U yt-dlp`

**Port already in use:**
- Default port is 5000
- Change in `web_preview.py` if needed
- Ensure no other service uses the port

**Termux-specific:**
- Storage permission: Run `termux-setup-storage`
- Python errors: `pkg reinstall python`
- Keep phone charged and screen timeout disabled

---

## 📈 Monitoring & Logs

**Check bot status:**
```bash
# View running processes
ps aux | grep bot.py

# Check logs (if using systemd/supervisor)
journalctl -u inert-bot -f
```

**Database check:**
```bash
# SQLite
sqlite3 bot_database.db "SELECT COUNT(*) FROM users;"

# MongoDB
mongo your-connection-string --eval "db.users.count()"
```

---

## 🔄 Updates & Maintenance

**Update bot:**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
# Restart bot service
```

**Backup database:**
```bash
# SQLite
cp bot_database.db bot_database_backup.db

# MongoDB
mongodump --uri="your-connection-string"
```

---

## 💡 Best Practices

1. ✅ Use environment variables for all secrets
2. ✅ Enable MongoDB for production (with backups)
3. ✅ Set up monitoring and alerts
4. ✅ Keep dependencies updated
5. ✅ Monitor storage usage (downloads folder)
6. ✅ Implement log rotation
7. ✅ Use HTTPS for web preview in production

---

## 🆘 Support

If you encounter issues:
- 📢 Check [@Theinertbotz](https://t.me/Theinertbotz) for updates
- 💬 Join [@Theinertbotzchart](https://t.me/Theinertbotzchart) for support
- 👨‍💻 Contact [@TheInertGuy](https://t.me/TheInertGuy) for technical help

---

## ⚠️ Important Reminders

- **Keep credits intact** - Respect the developer's work
- **Secure your credentials** - Never commit .env files
- **Monitor resources** - Watch disk space and bandwidth
- **Follow ToS** - Respect Telegram and YouTube policies
- **Backup regularly** - Prevent data loss

---

**Made with ❤️ by @TheInertGuy**
