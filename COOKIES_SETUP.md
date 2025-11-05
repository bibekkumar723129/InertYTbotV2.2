# 🍪 YouTube Cookies Setup Guide

This guide explains how to export YouTube cookies to fix the "Sign in to confirm you're not a bot" error.

## 📋 Why Do You Need Cookies?

YouTube sometimes blocks automated downloads by requesting sign-in verification. By using cookies from your browser session, the bot can bypass this restriction and download age-restricted or bot-protected videos.

---

## 🚀 Quick Setup

### Step 1: Export YouTube Cookies

**Method 1: Using Browser Extension (Recommended)**

1. **Install the Extension:**
   - **Chrome/Edge/Brave**: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - **Firefox**: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Cookies:**
   - Open [YouTube](https://www.youtube.com) in your browser
   - Make sure you're logged in to your YouTube account
   - Click the extension icon in your browser toolbar
   - Select "Export" or "Get cookies.txt"
   - Choose to export cookies for `youtube.com`
   - Save the file as `cookies.txt`

**Method 2: Using yt-dlp CLI**

```bash
# Export cookies from your default browser
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# For other browsers, replace 'chrome' with: firefox, edge, safari, opera, brave
```

### Step 2: Upload Cookies to Your Bot

#### **For Replit:**

1. In your Replit project, click on the "Files" icon
2. Upload `cookies.txt` to the root directory (same level as `main.py`)
3. The bot will automatically detect and use it on the next restart

#### **For Render:**

**Option A: Include in Repository**
1. Add `cookies.txt` to your Git repository root
2. Push to GitHub
3. Redeploy on Render

**Option B: Use Render Persistent Disk (Recommended for Production)**
1. Go to your Render dashboard
2. Navigate to your service
3. Click "Disks" tab
4. Create a new disk (e.g., `/data`)
5. Mount it to your service
6. Update `COOKIES_PATH` environment variable:
   ```
   COOKIES_PATH=/data/cookies.txt
   ```
7. Upload `cookies.txt` to the disk via SSH or SFTP

#### **For VPS/Dedicated Server:**

```bash
# Upload via SCP
scp cookies.txt user@your-server:/path/to/bot/cookies.txt

# Or upload via SFTP
sftp user@your-server
put cookies.txt /path/to/bot/cookies.txt
```

### Step 3: Configure Environment Variables

Add these to your `.env` file or Replit Secrets:

```env
USE_COOKIES=True
COOKIES_PATH=cookies.txt
```

**For Render:**
1. Go to your service → Environment
2. Add environment variables:
   - `USE_COOKIES` = `True`
   - `COOKIES_PATH` = `cookies.txt` (or `/data/cookies.txt` if using persistent disk)

### Step 4: Restart Your Bot

The bot will automatically detect and load the cookies on startup.

You should see this message in the logs:
```
✅ Cookies file found: cookies.txt
```

If cookies are not found, you'll see:
```
⚠️ No cookies found at cookies.txt. Some YouTube videos may require authentication.
```

---

## 🔒 Security Best Practices

### ⚠️ Important Security Notes:

1. **Never commit cookies.txt to public repositories**
   - The `.gitignore` file already excludes `cookies.txt`
   - Always verify before pushing to GitHub

2. **Cookies contain sensitive information:**
   - Your YouTube session tokens
   - Authentication credentials
   - Personal account data

3. **Use a dedicated YouTube account:**
   - Consider creating a separate YouTube account for the bot
   - Don't use your personal account if sharing the bot publicly

4. **Regularly update cookies:**
   - Cookies expire over time
   - Re-export and update every 30-60 days
   - If downloads start failing, try refreshing cookies

5. **For Render production:**
   - Use environment secrets or persistent disks
   - Never hardcode cookies in your code

---

## 🧪 Testing Your Setup

### Test 1: Check Cookies Detection

Look for this message in your bot logs on startup:
```
✅ Cookies file found: cookies.txt
```

### Test 2: Download a Protected Video

Try downloading a video that previously failed:
```
Send to bot: https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

If successful, the download will proceed without authentication errors.

### Test 3: Monitor Logs

Watch for this message during downloads:
```
🍪 Using cookies from: cookies.txt
```

---

## 🐛 Troubleshooting

### Issue: "No cookies found" warning

**Solution:**
- Verify `cookies.txt` exists in the correct location
- Check file permissions (should be readable)
- Ensure filename is exactly `cookies.txt` (case-sensitive on Linux)

### Issue: Downloads still fail with authentication error

**Solutions:**
1. **Re-export fresh cookies:**
   - Log in to YouTube in your browser
   - Export cookies again
   - Replace the old `cookies.txt`

2. **Verify cookie format:**
   - Open `cookies.txt` in a text editor
   - Should start with: `# Netscape HTTP Cookie File`
   - Should contain `.youtube.com` entries

3. **Check cookie expiration:**
   - Cookies expire after some time
   - Try logging in to YouTube and re-exporting

### Issue: Bot works locally but not on Render

**Solutions:**
1. **Verify file upload:**
   - Ensure `cookies.txt` is in the repository or persistent disk
   - Check Render logs for the file path

2. **Check environment variables:**
   - `USE_COOKIES` must be `True`
   - `COOKIES_PATH` must match actual file location

3. **Use absolute paths on Render:**
   ```env
   COOKIES_PATH=/opt/render/project/src/cookies.txt
   ```

---

## 📦 For Render Deployment

### Complete Render Setup:

1. **Add cookies.txt to your repository:**
   ```bash
   # In your local project
   git add cookies.txt
   git commit -m "Add YouTube cookies"
   git push origin main
   ```

2. **Set Environment Variables in Render:**
   - Go to Render Dashboard → Your Service → Environment
   - Add:
     - `USE_COOKIES` = `True`
     - `COOKIES_PATH` = `cookies.txt`

3. **Trigger Manual Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

4. **Verify in Logs:**
   - Check deployment logs for:
     ```
     ✅ Cookies file found: cookies.txt
     ```

### Alternative: Persistent Disk Method (For Long-term Production)

1. **Create a Persistent Disk:**
   - Render Dashboard → Your Service → Disks
   - Create disk: `/data`
   - Mount size: 1GB (minimum)

2. **Update Environment Variable:**
   ```env
   COOKIES_PATH=/data/cookies.txt
   ```

3. **Upload cookies via SSH/SFTP:**
   - Get SSH credentials from Render
   - Upload `cookies.txt` to `/data/cookies.txt`

---

## 🔄 Updating Cookies

### When to Update:

- Downloads start failing with authentication errors
- After 30-60 days (cookies expire)
- After logging out/in to YouTube
- After changing YouTube account password

### How to Update:

1. Export fresh cookies from your browser
2. Replace the old `cookies.txt` file
3. Restart your bot
4. Verify in logs: `✅ Cookies file found: cookies.txt`

---

## ✅ Verification Checklist

Before deploying to production, verify:

- [ ] Cookies exported from logged-in YouTube session
- [ ] `cookies.txt` uploaded to correct location
- [ ] `USE_COOKIES=True` in environment variables
- [ ] `COOKIES_PATH` points to correct file location
- [ ] Bot logs show "✅ Cookies file found"
- [ ] Test download works for restricted videos
- [ ] `.gitignore` includes `cookies.txt` (if public repo)

---

## 🆘 Need Help?

If you're still having issues:

1. Check bot logs for specific error messages
2. Verify YouTube cookies are valid (try in browser)
3. Test with a different YouTube account
4. Re-export cookies using a different browser
5. Contact support with:
   - Error message from logs
   - Hosting platform (Replit/Render/VPS)
   - Steps you've already tried

---

**Developer:** [@TheInertGuy](https://t.me/TheInertGuy)  
**Updates Channel:** [@Theinertbotz](https://t.me/Theinertbotz)  
**Support Group:** [@Theinertbotzchart](https://t.me/Theinertbotzchart)

⚠️ **Please don't remove credits - This bot was developed with care and effort!**
