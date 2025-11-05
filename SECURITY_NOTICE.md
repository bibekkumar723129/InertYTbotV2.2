# 🔒 Security Notice

## Session File Security

This project uses Pyrogram which creates session files (`*.session` and `*.session-journal`) containing authentication credentials.

### ⚠️ Important: These files are now in .gitignore

The `.gitignore` file has been updated to exclude:
- `*.session`
- `*.session-journal`

### 🛡️ Best Practices

1. **Never commit session files** to version control
2. **Rotate your bot token** if you suspect any exposure
3. **Keep your API credentials secure** in environment variables
4. Session files will be automatically recreated when the bot starts

### 🔄 How to Rotate Bot Token

If you need to rotate your bot token for security:

1. Open Telegram and find @BotFather
2. Send `/mybots`
3. Select your bot
4. Go to "Bot Settings" → "API Token"
5. Click "Revoke current token"
6. Copy the new token
7. Update `BOT_TOKEN` in your environment variables
8. Restart the bot

### ✅ What's Protected

The following are properly secured:
- API_ID and API_HASH (in Replit Secrets)
- BOT_TOKEN (in Replit Secrets)
- MONGO_URI (in Replit Secrets, if used)
- All session files (excluded from Git)

### 📝 Note

Session files are automatically regenerated when the bot starts with valid credentials. You don't need to manually create or manage them.
