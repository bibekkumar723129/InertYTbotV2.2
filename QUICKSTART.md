# 🚀 Quick Start Guide - 24/7 Bot Setup

## ✅ What's New

Your bot now includes:
- **Keep-Alive Server** with health check endpoints
- **Multi-Platform Support** (Replit, Render, Koyeb, Railway, Heroku, Fly.io)
- **Auto-Detection** of hosting platform
- **Improved Web Downloads** working across all platforms

---

## 📦 Files Added/Modified

### New Files
- ✨ **`keep_alive.py`** - Health check server for 24/7 operation
- 📖 **`UPTIMEROBOT_SETUP.md`** - Comprehensive setup guide
- 📋 **`QUICKSTART.md`** - This file

### Modified Files
- 🔧 **`main.py`** - Now runs bot with keep-alive
- 🌐 **`web_preview.py`** - Multi-platform URL detection

---

## ⚡ Quick Setup (3 Steps)

### 1️⃣ Get Your Bot URL

Run your bot and look for this in the console:

```
🔗 Public URL: https://workspace.newtestv47.repl.co
```

Or click the **Webview** button in Replit.

### 2️⃣ Set Up UptimeRobot

1. Go to [UptimeRobot.com](https://uptimerobot.com) (FREE)
2. Create account and add monitor:
   - **Type:** HTTP(s)
   - **URL:** Your bot URL (from step 1)
   - **Interval:** 5 minutes
3. Click "Create Monitor"

### 3️⃣ Done! 🎉

Your bot is now running 24/7! UptimeRobot will ping it every 5 minutes.

---

## 🔍 Test Your Setup

### Check Health Endpoints

```bash
# Simple check
curl https://your-url.repl.co/

# Detailed check
curl https://your-url.repl.co/health

# Ping check
curl https://your-url.repl.co/ping
```

**Expected Responses:**
- `/` → `✅ Bot is alive!`
- `/health` → JSON with status, platform, timestamp
- `/ping` → `pong`

---

## 📱 How to Run

### Option 1: Using main.py (Recommended)

```bash
python main.py
```

This runs the bot WITH keep-alive server.

### Option 2: Using bot.py (Legacy)

```bash
python bot.py
```

This runs the bot WITHOUT keep-alive server (not recommended for 24/7).

---

## 🌐 Platform-Specific URLs

Your bot auto-detects the platform and generates correct URLs:

| Platform | URL Format | Auto-Detected |
|----------|------------|---------------|
| **Replit** | `https://repl-name.username.repl.co` | ✅ Yes |
| **Render** | `https://service-name.onrender.com` | ✅ Yes |
| **Koyeb** | `https://app-name.koyeb.app` | ✅ Yes |
| **Railway** | `https://app-name.railway.app` | ✅ Yes |
| **Heroku** | `https://app-name.herokuapp.com` | ✅ Yes |
| **Fly.io** | `https://app-name.fly.dev` | ✅ Yes |

---

## 🎯 Key Features

### 1. Multi-Platform Web Downloads
- Downloads work on ANY hosting platform
- Auto-generates correct URLs
- No manual configuration needed

### 2. Health Check Endpoints
- `/` - Simple text response
- `/health` - JSON with detailed info
- `/ping` - Minimal ping response

### 3. 24/7 Uptime
- UptimeRobot keeps bot alive
- Email alerts if bot goes down
- Works on free hosting tiers

### 4. Zero Configuration
- Platform auto-detection
- No environment variables needed
- Works out of the box

---

## 🔧 Environment Variables (Optional)

The bot auto-detects your platform, but you can override:

```bash
# Replit (auto-set)
REPL_SLUG=your-repl-name
REPL_OWNER=your-username

# Render (auto-set)
RENDER_SERVICE_NAME=your-service

# Custom Port (default: 5000)
PORT=5000
```

---

## 📊 What You'll See

### Console Output

```
============================================================
🚀 Starting Inert Downloader Bot...
============================================================
📊 Database: SQLITE
💾 Storage Channel: -1003292407667
⚙️  Free Download Limit: 2/day
============================================================

============================================================
🌐 Keep-Alive Server Starting...
📍 Platform: Replit
🔗 Public URL: https://workspace.newtestv47.repl.co
💚 Health Check: https://workspace.newtestv47.repl.co/health
🏓 Ping Endpoint: https://workspace.newtestv47.repl.co/ping
============================================================

📌 Add this URL to UptimeRobot to keep bot running 24/7:
   https://workspace.newtestv47.repl.co
============================================================

============================================================
✅ Bot is now running!
💡 Keep this window open or use a process manager
============================================================
```

---

## ❓ Troubleshooting

### Bot URL Not Working?

1. **Check Console** - Look for the "Public URL" line
2. **Test Locally** - `curl http://localhost:5000/`
3. **Wait 30 seconds** - Platform might be waking up

### UptimeRobot Shows Down?

1. **Increase Timeout** - Set to 60 seconds in UptimeRobot
2. **Check Bot Console** - Look for errors
3. **Verify URL** - Test in browser first

### Web Downloads Failing?

1. **Check Platform Detection** - Console shows detected platform
2. **Verify URL Format** - Should match your hosting platform
3. **Check Logs** - Look for download errors

---

## 📚 Full Documentation

For detailed setup instructions, see:
- **[UPTIMEROBOT_SETUP.md](UPTIMEROBOT_SETUP.md)** - Complete guide with all platforms

---

## 📞 Support

**Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
**Updates:** [@Theinertbotz](https://t.me/Theinertbotz)  
**Support:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

---

**⚠️ PLEASE DON'T REMOVE CREDITS ⚠️**

This enhancement was made to improve your bot's reliability and reach.  
Credits and developer information must remain intact.

---

*Happy Hosting! 🎉*
