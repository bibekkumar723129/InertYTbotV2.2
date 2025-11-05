# 🤖 24/7 Bot Setup Guide - UptimeRobot + Hosting Platforms

> Keep your Telegram bot running 24/7 for FREE using UptimeRobot pinging!

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Platform-Specific Setup](#-platform-specific-setup)
3. [UptimeRobot Configuration](#-uptimerobot-configuration)
4. [Verification & Testing](#-verification--testing)
5. [Safety Tips & Best Practices](#-safety-tips--best-practices)
6. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

Your bot now includes a **keep-alive server** that runs alongside your Telegram bot. This server provides health check endpoints that UptimeRobot can ping every 5 minutes to keep your bot alive.

### How It Works

1. **Flask Web Server** runs on the same instance as your bot
2. **Health Check Endpoints** (`/`, `/health`, `/ping`) respond with status
3. **UptimeRobot** pings these endpoints every 5 minutes
4. **Your Bot Stays Alive** as long as it receives regular pings

---

## 🌐 Platform-Specific Setup

### 🔷 Replit

#### Step 1: Get Your Replit URL

When you run your bot on Replit, you'll see the URL displayed in the console:

```
🌐 Keep-Alive Server Starting...
📍 Platform: Replit
🔗 Public URL: https://your-repl.your-username.repl.co
```

**Alternative Method:**
1. Click the **"Webview"** button (🌐) in the top right of your Repl
2. Click **"Open in new tab"**
3. Copy the URL from your browser (format: `https://your-repl.your-username.repl.co`)

**Environment Variables (Auto-detected):**
- `REPL_SLUG` - Your repl name
- `REPL_OWNER` - Your username

#### Step 2: Configure Replit for Always-On (Optional)

**Free Tier:**
- Repls sleep after inactivity
- UptimeRobot pinging keeps it awake during active hours
- May still sleep during quiet periods

**Recommended: Reserved VM Deployment** (Paid)
- Always-on cloud server
- No sleep/interruptions
- Perfect for production bots
- Configure via the "Publish" tool in Replit

---

### 🟢 Render

#### Get Your Render URL

1. Deploy your bot on Render
2. Your service URL will be: `https://your-service-name.onrender.com`
3. Find it in: **Dashboard → Your Service → URL**

**Environment Variable (Auto-set):**
- `RENDER` - Automatically set by Render
- `RENDER_SERVICE_NAME` - Your service name

**Important for Render:**
- Free tier services sleep after 15 minutes of inactivity
- UptimeRobot pinging prevents sleep
- Render may take 30-60 seconds to wake up from sleep
- Set UptimeRobot interval to **5 minutes** minimum

---

### 🔵 Koyeb

#### Get Your Koyeb URL

1. Deploy your bot on Koyeb
2. Your app URL: `https://your-app.koyeb.app`
3. Find it in: **Services → Your App → Public URL**

**Environment Variable (Auto-set):**
- `KOYEB_PUBLIC_DOMAIN` - Your public domain

**Koyeb Advantages:**
- Free tier doesn't sleep
- Excellent for 24/7 bots
- Fast response times

---

### 🟣 Railway

#### Get Your Railway URL

1. Deploy to Railway
2. Generate a domain in: **Settings → Networking → Generate Domain**
3. Your URL: `https://your-app.railway.app`

**Environment Variables (Auto-set):**
- `RAILWAY_ENVIRONMENT` - Current environment
- `RAILWAY_STATIC_URL` or `RAILWAY_PUBLIC_DOMAIN` - Your public URL

---

### 🟠 Heroku

#### Get Your Heroku URL

1. Deploy to Heroku
2. Your app URL: `https://your-app-name.herokuapp.com`
3. Find it in: **Dashboard → Your App → Open app**

**Environment Variable (Auto-set):**
- `HEROKU_APP_NAME` - Your app name

**Important for Heroku:**
- Free tier discontinued (now requires payment)
- Eco dynos sleep after 30 minutes
- UptimeRobot helps prevent sleep

---

### 🪂 Fly.io

#### Get Your Fly.io URL

1. Deploy to Fly.io
2. Your app URL: `https://your-app.fly.dev`
3. Run: `fly status` to see your URL

**Environment Variable (Auto-set):**
- `FLY_APP_NAME` - Your app name

---

## 🔔 UptimeRobot Configuration

### Step 1: Create UptimeRobot Account

1. Go to [UptimeRobot.com](https://uptimerobot.com)
2. Sign up for a **FREE account**
3. Verify your email

### Step 2: Add New Monitor

1. Click **"+ Add New Monitor"**
2. Fill in the details:

   | Field | Value |
   |-------|-------|
   | **Monitor Type** | HTTP(s) |
   | **Friendly Name** | Your Bot Name (e.g., "Inert Downloader Bot") |
   | **URL** | Your platform URL (see above) |
   | **Monitoring Interval** | 5 minutes (free tier) |

3. **Advanced Settings (Optional):**
   - **Timeout:** 30 seconds (recommended)
   - **HTTP Method:** GET
   - **Expected Status Code:** 200

4. Click **"Create Monitor"**

### Step 3: Verify Monitor

1. Wait 5-10 minutes
2. Check UptimeRobot dashboard
3. Status should show **"Up"** with a green indicator
4. You'll receive email alerts if your bot goes down

### Alternative Health Check Endpoints

You can use any of these endpoints for UptimeRobot:

| Endpoint | Response | Best For |
|----------|----------|----------|
| `/` | `✅ Bot is alive!` | Simple text check |
| `/health` | JSON with status & timestamp | Detailed monitoring |
| `/ping` | `pong` | Minimal overhead |

**Example URLs:**
- `https://your-repl.username.repl.co/`
- `https://your-repl.username.repl.co/health`
- `https://your-repl.username.repl.co/ping`

---

## ✅ Verification & Testing

### Test Your Health Check Endpoint

Open your URL in a browser or use `curl`:

```bash
curl https://your-repl.username.repl.co/
# Expected: ✅ Bot is alive!

curl https://your-repl.username.repl.co/health
# Expected: JSON with status, timestamp, platform
```

**Expected Response:**
```
✅ Bot is alive!
```

**JSON Health Check Response:**
```json
{
  "status": "online",
  "message": "Bot is running smoothly",
  "timestamp": "2025-11-05T10:30:00.123456",
  "platform": "Replit"
}
```

### Check Bot Console

Your bot should display:

```
============================================================
🌐 Keep-Alive Server Starting...
📍 Platform: Replit
🔗 Public URL: https://your-repl.username.repl.co
💚 Health Check: https://your-repl.username.repl.co/health
🏓 Ping Endpoint: https://your-repl.username.repl.co/ping
============================================================

📌 Add this URL to UptimeRobot to keep bot running 24/7:
   https://your-repl.username.repl.co
============================================================
```

---

## ⚠️ Safety Tips & Best Practices

### 🔒 Resource Management

1. **File Cleanup:**
   - Bot automatically cleans up downloaded files
   - Monitor disk usage regularly
   - Set download limits for free users

2. **Memory Usage:**
   - Keep-alive server uses minimal resources (<50MB RAM)
   - Monitor memory if handling large files
   - Implement file size limits (already configured)

3. **Bandwidth:**
   - UptimeRobot pings every 5 minutes (~8,640 pings/month)
   - Each ping uses ~1KB bandwidth
   - Total: ~8.5MB/month (negligible)

### 📊 File Size Limits (Pre-configured)

| User Type | Max File Size | Daily Limit |
|-----------|---------------|-------------|
| **Free** | 100 MB | 2 downloads |
| **Premium** | 2 GB | Unlimited |
| **Large Files** | >2 GB | Auto-split into 1.8GB parts |

### 🛡️ Security Best Practices

1. **Keep API Keys Secret:**
   - Never commit `.env` file to Git
   - Use environment variables for sensitive data
   - Replit Secrets are encrypted

2. **Rate Limiting:**
   - Bot has built-in download limits
   - Prevents abuse and excessive resource usage

3. **Monitoring:**
   - UptimeRobot sends email alerts if bot goes down
   - Check logs regularly for errors
   - Monitor database size if using MongoDB/SQLite

### 📁 Storage Considerations

#### Replit
- Free: 10 GB storage
- Keep `downloads/` folder clean
- Files auto-delete after upload

#### Render
- Free: 1 GB ephemeral storage
- Files deleted on restart
- Use external storage for persistence

#### Koyeb
- Free: 2.5 GB storage
- Persistent storage available

#### Railway
- Free: 1 GB storage (deprecated)
- Paid plans have larger limits

---

## 🔧 Troubleshooting

### ❌ UptimeRobot Shows "Down"

**Possible Causes:**

1. **Bot Crashed:**
   - Check console for errors
   - Restart the bot
   - Check error logs

2. **Platform Sleeping:**
   - Wait 30-60 seconds for platform to wake
   - Increase UptimeRobot timeout to 60 seconds
   - Consider upgrading to paid tier for always-on

3. **Wrong URL:**
   - Verify URL in browser first
   - Check for typos
   - Ensure URL matches console output

4. **Port Issues:**
   - Bot should run on port 5000 (auto-configured)
   - Check if port is exposed

### 🐛 Bot Not Responding to Telegram

**Checks:**

1. **Telegram Connection:**
   ```
   Check console for: "✅ Bot is running!"
   ```

2. **API Credentials:**
   - Verify `API_ID`, `API_HASH`, `BOT_TOKEN` in `.env`
   - Get new token from [@BotFather](https://t.me/BotFather) if needed

3. **Database Connection:**
   ```
   Check console for: "📊 Database: SQLITE" or "MONGODB"
   ```

### 🌐 Web Download Links Not Working

**Solutions:**

1. **Check Platform Detection:**
   - Console shows detected platform
   - Verify correct environment variables are set

2. **Manual Override (if needed):**
   ```bash
   # For Replit
   export REPL_SLUG=your-repl-name
   export REPL_OWNER=your-username
   
   # For Render
   export RENDER_SERVICE_NAME=your-service-name
   ```

3. **Test Download Endpoint:**
   ```bash
   # Should return 404 (expected for invalid token)
   curl https://your-url/download/test-token
   ```

### 📱 Bot Works Locally But Not on Platform

**Common Issues:**

1. **Environment Variables:**
   - Add all required secrets
   - Check `.env` file is not in `.gitignore` (if using dotenv)
   - Use platform's secrets manager

2. **Dependencies:**
   - Run: `pip install -r requirements.txt`
   - Ensure all packages are listed

3. **Port Configuration:**
   - Use port from environment: `PORT` env var
   - Default: 5000

---

## 📞 Support & Credits

**Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
**Updates:** [@Theinertbotz](https://t.me/Theinertbotz)  
**Support Group:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

---

## 🎉 Success Checklist

- [ ] Bot running on your chosen platform
- [ ] Health check endpoint accessible (`/`, `/health`, or `/ping`)
- [ ] UptimeRobot monitor created and showing "Up"
- [ ] Email alerts configured in UptimeRobot
- [ ] Bot responding to Telegram commands
- [ ] Web downloads working correctly
- [ ] Monitoring interval set to 5 minutes

**Congratulations! Your bot is now running 24/7! 🚀**

---

## 🔄 Regular Maintenance

### Weekly
- [ ] Check UptimeRobot uptime percentage (should be >99%)
- [ ] Review error logs
- [ ] Monitor disk usage

### Monthly
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Check for security updates
- [ ] Review and clean old database entries
- [ ] Backup important data

---

**⚠️ PLEASE DON'T REMOVE CREDITS ⚠️**

This bot was developed with care and effort by [@TheInertGuy](https://t.me/TheInertGuy).  
If you find it useful, please keep the credits intact and consider supporting the developer!

---

*Last Updated: November 2025*
