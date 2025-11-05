"""
Keep-alive server for 24/7 bot operation
Works with UptimeRobot for free hosting on Replit/Render/Railway
"""

from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "service": "Inert Downloader Bot",
        "platform": detect_platform()
    }

@app.route('/ping')
def ping():
    return "pong"

def detect_platform():
    """Detect which hosting platform the bot is running on"""
    if os.environ.get('REPL_ID'):
        return "Replit"
    elif os.environ.get('RENDER'):
        return "Render"
    elif os.environ.get('KOYEB_PUBLIC_DOMAIN'):
        return "Koyeb"
    elif os.environ.get('RAILWAY_ENVIRONMENT'):
        return "Railway"
    elif os.environ.get('HEROKU_APP_NAME'):
        return "Heroku"
    elif os.environ.get('FLY_APP_NAME'):
        return "Fly.io"
    else:
        return "Local"

def run():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def keep_alive():
    """Start the keep-alive server in a background thread"""
    t = threading.Thread(target=run, daemon=True)
    t.start()
    print("🌐 Keep-alive server started on http://0.0.0.0:8080")
