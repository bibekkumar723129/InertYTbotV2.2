
from flask import Flask, render_template_string, send_file, abort
import threading
import os
from pathlib import Path

app = Flask(__name__)

# Store temporary download tokens
download_tokens = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheInertGuy - Bot Preview</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 600px;
            width: 90%;
        }
        
        h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3),
                             0 0 10px rgba(255, 255, 255, 0.4);
            }
            to {
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3),
                             0 0 20px rgba(255, 255, 255, 0.8),
                             0 0 30px rgba(255, 255, 255, 0.6);
            }
        }
        
        .subtitle {
            font-size: 1.5em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .bot-info {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .bot-info p {
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        .telegram-btn {
            display: inline-block;
            margin-top: 20px;
            padding: 15px 40px;
            background: #0088cc;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 136, 204, 0.4);
        }
        
        .telegram-btn:hover {
            background: #006699;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 136, 204, 0.6);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TheInertGuy</h1>
        <div class="subtitle">🤖 Inert Downloader Bot</div>
        
        <div class="bot-info">
            <p>✨ YouTube Video & Audio Downloader</p>
            <p>💎 Premium Features Available</p>
            <p>🚀 Fast & Reliable Downloads</p>
            <p>📱 Easy to Use</p>
        </div>
        
        <a href="https://t.me/InertYTbot" class="telegram-btn" target="_blank">
            📲 Open in Telegram
        </a>
        
        <div style="margin-top: 40px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <h3 style="color: #fff; margin-bottom: 10px;">👨‍💻 Developer Credits</h3>
            <p style="color: #ddd;">Developer: <a href="https://t.me/TheInertGuy" style="color: #61dafb;">@TheInertGuy</a></p>
            <p style="color: #ddd;">Updates: <a href="https://t.me/Theinertbotz" style="color: #61dafb;">@Theinertbotz</a></p>
            <p style="color: #ddd;">Support: <a href="https://t.me/Theinertbotzchart" style="color: #61dafb;">@Theinertbotzchart</a></p>
            <p style="color: #ff6b6b; margin-top: 10px; font-size: 12px;">⚠️ Please don't remove credits</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download/<token>')
def download_file(token):
    """Serve file for download via web"""
    try:
        if token not in download_tokens:
            print(f"❌ Invalid or expired download token: {token}")
            abort(404, description="Download link expired or invalid")
        
        file_info = download_tokens[token]
        filepath = file_info['path']
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            abort(404, description="File not found on server")
        
        filename = file_info.get('filename', os.path.basename(filepath))
        print(f"✅ Serving file: {filename} ({filepath})")
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        print(f"❌ Error serving download: {e}")
        import traceback
        traceback.print_exc()
        abort(500, description="Server error while preparing download")

def start_web_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

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

def get_base_url():
    """Get the base URL based on the hosting platform"""
    platform = detect_platform()
    
    if platform == "Replit":
        repl_slug = os.environ.get('REPL_SLUG', 'bot')
        repl_owner = os.environ.get('REPL_OWNER', 'user')
        return f"https://{repl_slug}.{repl_owner}.repl.co"
    
    elif platform == "Render":
        render_service = os.environ.get('RENDER_SERVICE_NAME', 'bot')
        return f"https://{render_service}.onrender.com"
    
    elif platform == "Koyeb":
        return os.environ.get('KOYEB_PUBLIC_DOMAIN', 'https://your-app.koyeb.app')
    
    elif platform == "Railway":
        railway_domain = os.environ.get('RAILWAY_STATIC_URL') or os.environ.get('RAILWAY_PUBLIC_DOMAIN')
        if railway_domain:
            if railway_domain.startswith(('http://', 'https://')):
                return railway_domain
            return f"https://{railway_domain}"
        return "https://your-app.railway.app"
    
    elif platform == "Heroku":
        app_name = os.environ.get('HEROKU_APP_NAME', 'bot')
        return f"https://{app_name}.herokuapp.com"
    
    elif platform == "Fly.io":
        app_name = os.environ.get('FLY_APP_NAME', 'bot')
        return f"https://{app_name}.fly.dev"
    
    else:
        return "http://localhost:5000"

def generate_download_link(filepath: str, filename: str) -> str:
    """Generate a unique download token and return the download URL"""
    import uuid
    token = str(uuid.uuid4())
    download_tokens[token] = {
        'path': filepath,
        'filename': filename
    }
    
    base_url = get_base_url()
    return f"{base_url}/download/{token}"

def cleanup_download_token(token: str):
    """Remove a download token after use"""
    if token in download_tokens:
        del download_tokens[token]

def run_web_preview():
    thread = threading.Thread(target=start_web_server, daemon=True)
    thread.start()
