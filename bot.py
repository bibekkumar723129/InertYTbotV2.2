"""
╔══════════════════════════════════════════════════════════╗
║           Inert Downloader Bot                           ║
║                                                          ║
║  Developer: @TheInertGuy                                 ║
║  Updates Channel: @Theinertbotz                          ║
║  Support Group: @Theinertbotzchart                       ║
║                                                          ║
║  ⚠️  DO NOT REMOVE CREDITS  ⚠️                           ║
║  This bot was developed with care and effort.            ║
║  Please respect the developer by keeping credits intact. ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from pyrogram.errors import FloodWait
from datetime import datetime

from config import Config
from database import db
from downloader import downloader
from utils import (
    format_filesize,
    format_duration,
    cleanup_file,
    get_download_progress_text,
    check_file_size,
    escape_markdown,
    download_thumbnail,
    create_progress_bar,
    format_eta
)
from file_splitter import split_file, cleanup_parts
from web_preview import run_web_preview, generate_download_link, cleanup_download_token

app = Client(
    "inert_downloader_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

user_downloads = {}

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )

    welcome_text = f"""
👋 **Welcome to Inert Downloader Bot!**

🎥 I can download YouTube videos and audio for you!

**Available Commands:**
/download - Download a video or audio
/premium - View premium plans
/help - Get help and information
/stats - View your statistics

**Features:**
✅ Multiple quality options (144p - 1080p)
🎵 Audio-only downloads
💎 Premium membership available
📊 Download tracking

Send me a YouTube link or use /download to get started!

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Developer:** @TheInertGuy
📢 **Updates:** @Theinertbotz
💬 **Support:** @Theinertbotzchart
━━━━━━━━━━━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Get Premium", callback_data="premium")],
        [InlineKeyboardButton("📖 Help", callback_data="help")]
    ])

    await message.reply_text(welcome_text, reply_markup=keyboard)

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = """
📖 **Help & Information**

**How to use:**
1️⃣ Send me a YouTube link
2️⃣ Choose your preferred quality
3️⃣ Wait for the download to complete
4️⃣ Receive your file!

**Free Users:**
• 2 downloads per day
• Max file size: 100MB
• Standard quality options

**Premium Users:**
• ∞ Unlimited downloads
• Max file size: 2GB (auto-split for larger files)
• File rename feature
• Link preview with thumbnails
• Priority downloads
• Files >2GB split into 1.8GB parts

**Commands:**
/download - Start a download
/premium - View premium plans
/stats - Your statistics
/help - This message

**Supported Sites:**
YouTube, YouTube Music, and more!

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Developer:** @TheInertGuy
📢 **Updates:** @Theinertbotz
💬 **Support:** @Theinertbotzchart

⚠️ **Please don't remove credits!**
━━━━━━━━━━━━━━━━━━━━━━━━
"""

    await message.reply_text(help_text)

@app.on_message(filters.command("stats"))
async def stats_command(client: Client, message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )
        user = await db.get_user(message.from_user.id)

    stats = await db.get_user_stats(message.from_user.id)

    status = "💎 Premium" if stats.get('is_premium') else "🆓 Free"

    stats_text = f"""
📊 **Your Statistics**

👤 User: {message.from_user.first_name}
🎫 Status: {status}
📥 Total Downloads: {stats.get('total_downloads', 0)}
📆 Today's Downloads: {stats.get('downloads_today', 0)}
⏳ Remaining Today: {stats.get('downloads_remaining', 0)}
"""

    if stats.get('is_premium') and stats.get('premium_expires'):
        stats_text += f"\n⏰ Premium Expires: {stats['premium_expires']}"

    await message.reply_text(stats_text)

@app.on_message(filters.command("premium"))
async def premium_command(client: Client, message: Message):
    await show_premium_page(message)

async def show_premium_page(message: Message):
    premium_text = """
💎 **Premium Membership**

**Premium Features:**
✨ Unlimited daily downloads
📁 Extended file size limit (2GB)
✏️ File rename feature
🔍 Link preview & thumbnails
⚡ Priority download queue
🎯 Access to all quality options
📦 Auto-split for files >2GB

**Subscription Plans:**
1️⃣ 1 Month - $5
3️⃣ 3 Months - $12
6️⃣ 6 Months - $20
🎉 1 Year - $35

**How to Subscribe:**
1. Choose a plan below
2. Scan the QR code to pay
3. Send payment proof to admin
4. Get instant premium access!

Contact admin for manual activation.

━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Developer:** @TheInertGuy
📢 **Updates:** @Theinertbotz
💬 **Support:** @Theinertbotzchart
━━━━━━━━━━━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 View Payment QR", callback_data="payment_qr")],
        [InlineKeyboardButton("👤 Contact Admin", url="https://t.me/darkworld008")]
    ])

    await message.reply_text(premium_text, reply_markup=keyboard)

@app.on_message(filters.command("download"))
async def download_command(client: Client, message: Message):
    await message.reply_text(
        "📎 Please send me a YouTube link to download!\n\n"
        "Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

@app.on_message(filters.command("add_premium") & filters.user(Config.ADMIN_IDS))
async def add_premium_command(client: Client, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.reply_text(
                "❌ Usage: /add_premium <user_id> <days>\n"
                "Example: /add_premium 123456789 30"
            )
            return

        user_id = int(parts[1])
        days = int(parts[2])

        user = await db.get_user(user_id)
        if not user:
            await message.reply_text("❌ User not found in database!")
            return

        await db.add_premium(user_id, days)

        await message.reply_text(
            f"✅ Successfully added {days} days of premium to user {user_id}!"
        )

        try:
            await client.send_message(
                user_id,
                f"🎉 **Congratulations!**\n\n"
                f"You have been granted {days} days of premium membership!\n"
                f"Enjoy unlimited downloads and premium features! 💎"
            )
        except:
            pass

    except ValueError:
        await message.reply_text("❌ Invalid user_id or days. Please use numbers.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r'(youtube\.com|youtu\.be)'))
async def handle_youtube_link(client: Client, message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )

    can_download = await db.check_download_limit(message.from_user.id)

    if not can_download:
        is_premium = await db.is_premium(message.from_user.id)
        if not is_premium:
            await message.reply_text(
                "❌ **Download Limit Reached!**\n\n"
                f"Free users can download {Config.FREE_DOWNLOAD_LIMIT} files per day.\n"
                "Your limit will reset tomorrow.\n\n"
                "💎 Upgrade to Premium for unlimited downloads!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("💎 Get Premium", callback_data="premium")
                ]])
            )
            return

    url = message.text

    status_msg = await message.reply_text("🔍 Fetching video information...")

    try:
        info = await downloader.get_video_info(url)

        if not info:
            await status_msg.edit_text("❌ Failed to fetch video information. Please check the URL.")
            return

        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        thumbnail = info.get('thumbnail', '')

        is_premium = await db.is_premium(message.from_user.id)

        info_text = f"🎬 **{title}**\n\n"

        if is_premium:
            info_text += f"👤 Uploader: {uploader}\n"
            info_text += f"⏱ Duration: {format_duration(duration)}\n\n"

        info_text += "📥 Select quality to download:"

        formats = await downloader.get_available_formats(url)

        if not formats:
            await status_msg.edit_text("❌ No formats available for this video.")
            return

        user_downloads[message.from_user.id] = {
            'url': url,
            'title': title,
            'formats': formats,
            'thumbnail': thumbnail
        }

        keyboard_buttons = []
        for fmt in formats:
            quality = fmt['quality']
            size = format_filesize(fmt['filesize']) if fmt['filesize'] else "Unknown"
            button_text = f"{quality} ({size})" if fmt['filesize'] else quality
            callback_data = f"dl_{fmt['type']}_{fmt['format_id']}"
            keyboard_buttons.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

        keyboard = InlineKeyboardMarkup(keyboard_buttons)

        if thumbnail and is_premium:
            try:
                await status_msg.delete()
                await message.reply_photo(
                    photo=thumbnail,
                    caption=info_text,
                    reply_markup=keyboard
                )
            except:
                await status_msg.edit_text(info_text, reply_markup=keyboard)
        else:
            await status_msg.edit_text(info_text, reply_markup=keyboard)

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")

@app.on_callback_query(filters.regex(r'^dl_'))
async def handle_download_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_downloads:
        await callback_query.answer("❌ Session expired. Please send the link again.", show_alert=True)
        return

    data = callback_query.data.split('_')
    format_type = data[1]
    format_id = '_'.join(data[2:])

    download_data = user_downloads[user_id]
    url = download_data['url']
    title = download_data['title']

    is_premium = await db.is_premium(user_id)

    if is_premium and 'awaiting_rename' not in download_data:
        user_downloads[user_id]['awaiting_rename'] = True
        user_downloads[user_id]['format_type'] = format_type
        user_downloads[user_id]['format_id'] = format_id

        await callback_query.answer()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Rename File", callback_data="rename_prompt")],
            [InlineKeyboardButton("⬇️ Download with Original Name", callback_data="download_original")]
        ])

        await callback_query.message.edit_text(
            f"📁 **File Name Options**\n\n"
            f"Current name: `{title}`\n\n"
            f"💎 As a premium user, you can rename this file before download.\n\n"
            f"Choose an option:",
            reply_markup=keyboard
        )
        return

    await callback_query.answer("⬇️ Starting download...")

    status_msg = await callback_query.message.edit_text("📥 Starting download...")

    try:
        # Create progress callback with download tracking
        download_stats = {'last_update': 0, 'start_time': __import__('time').time()}
        loop = asyncio.get_running_loop()

        def progress_hook(d):
            import time
            now = time.time()
            if d.get('status') == 'downloading' and now - download_stats['last_update'] >= 2:
                download_stats['last_update'] = now
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    
                    if total > 0:
                        percent = int((downloaded / total) * 100)
                        speed = d.get('speed', 0)
                        speed_mb = (speed / (1024 * 1024)) if speed else 0
                        eta = d.get('eta', 0) or 0

                        progress_text = f"📥 Download: {create_progress_bar(percent)} {percent}%\n"
                        progress_text += f"📤 Upload:   {create_progress_bar(0)} 0%\n\n"
                        progress_text += f"💾 {int(downloaded / (1024 * 1024))}MB / {int(total / (1024 * 1024))}MB | "
                        progress_text += f"⚡ {speed_mb:.1f}MB/s | ⏱ ETA: {format_eta(eta)}"

                        async def update_progress():
                            try:
                                await status_msg.edit_text(progress_text)
                            except:
                                pass
                        
                        asyncio.run_coroutine_threadsafe(update_progress(), loop)
                except:
                    pass

        filepath = await downloader.download_media(
            url,
            format_id,
            progress_callback=progress_hook,
            format_type=format_type
        )

        if not filepath or not os.path.exists(filepath):
            await status_msg.edit_text(
                "❌ **Download Failed**\n\n"
                "Possible reasons:\n"
                "• Video is unavailable or private\n"
                "• Network connection issue\n"
                "• Invalid format selected\n\n"
                "Please try again or select a different quality."
            )
            return

        is_premium = await db.is_premium(user_id)
        max_size = Config.PREMIUM_MAX_SIZE_MB if is_premium else Config.FREE_MAX_SIZE_MB

        size_ok, file_size_mb = await check_file_size(filepath, max_size)

        if not size_ok:
            cleanup_file(filepath)
            await status_msg.edit_text(
                f"❌ File too large ({file_size_mb}MB)!\n\n"
                f"Your limit: {max_size}MB\n"
                "💎 Upgrade to Premium for larger files!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("💎 Get Premium", callback_data="premium")
                ]])
            )
            return

        await upload_and_send_file(client, user_id, filepath, title, format_type, status_msg, callback_query)

        await db.increment_downloads(user_id)

        if user_id in user_downloads:
            del user_downloads[user_id]

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await status_msg.edit_text("⏳ Rate limited. Please try again in a moment.")
    except Exception as e:
        print(f"Download error: {e}")
        await status_msg.edit_text(f"❌ Error during download: {str(e)}")
        if 'filepath' in locals():
            cleanup_file(filepath)

@app.on_callback_query(filters.regex(r'^rename_prompt$'))
async def rename_prompt_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_downloads:
        await callback_query.answer("❌ Session expired.", show_alert=True)
        return

    await callback_query.answer()
    user_downloads[user_id]['waiting_for_filename'] = True

    await callback_query.message.edit_text(
        "✏️ **Rename File**\n\n"
        "Please send the new filename (without extension).\n"
        "The extension will be added automatically.\n\n"
        "Example: `My Cool Video` or `Awesome Song`\n\n"
        "Send /cancel to cancel."
    )

@app.on_callback_query(filters.regex(r'^download_original$'))
async def download_original_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_downloads:
        await callback_query.answer("❌ Session expired.", show_alert=True)
        return

    download_data = user_downloads[user_id]
    format_type = download_data.get('format_type')
    format_id = download_data.get('format_id')
    url = download_data['url']
    title = download_data['title']

    await callback_query.answer("⬇️ Starting download...")
    status_msg = await callback_query.message.edit_text(
        f"⏳ **Preparing Download...**\n\n"
        f"📁 {title}\n"
        f"📊 Quality: {format_type.title()}\n\n"
        f"Please wait..."
    )

    try:
        await status_msg.edit_text(
            f"📥 **Downloading...**\n\n"
            f"📁 {title}\n"
            f"📊 Quality: {format_type.title()}\n\n"
            f"This may take a moment..."
        )
        
        filepath = await downloader.download_media(
            url,
            format_id,
            progress_callback=None,
            format_type=format_type
        )

        if not filepath or not os.path.exists(filepath):
            await status_msg.edit_text(
                "❌ **Download Failed**\n\n"
                "Possible reasons:\n"
                "• Video is unavailable or private\n"
                "• Network connection issue\n"
                "• Invalid format selected\n\n"
                "Please try again or select a different quality."
            )
            return

        await status_msg.edit_text(
            f"✅ **Download Complete!**\n\n"
            f"📁 {title}\n"
            f"Preparing your file..."
        )
        
        await upload_and_send_file(client, user_id, filepath, title, format_type, status_msg, callback_query)

    except Exception as e:
        print(f"Download error: {e}")
        await status_msg.edit_text(f"❌ Error during download: {str(e)}")
        if 'filepath' in locals() and filepath:
            cleanup_file(filepath)

@app.on_message(filters.text & filters.private & ~filters.command(['start', 'download', 'help', 'stats', 'premium', 'add_premium', 'cancel']))
async def handle_rename_input(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_downloads:
        return

    if not user_downloads[user_id].get('waiting_for_filename'):
        return

    download_data = user_downloads[user_id]
    new_filename = message.text.strip()

    if len(new_filename) > 100:
        await message.reply_text("❌ Filename too long. Please keep it under 100 characters.")
        return

    user_downloads[user_id]['custom_filename'] = new_filename
    user_downloads[user_id]['waiting_for_filename'] = False

    format_type = download_data.get('format_type')
    format_id = download_data.get('format_id')
    url = download_data['url']

    status_msg = await message.reply_text(
        f"⏳ **Preparing Download...**\n\n"
        f"📁 {new_filename}\n"
        f"Please wait..."
    )

    try:
        await status_msg.edit_text(
            f"📥 **Downloading...**\n\n"
            f"📁 {new_filename}\n"
            f"This may take a moment..."
        )
        
        filepath = await downloader.download_media(
            url,
            format_id,
            progress_callback=None,
            format_type=format_type
        )

        if not filepath or not os.path.exists(filepath):
            await status_msg.edit_text(
                "❌ **Download Failed**\n\n"
                "Possible reasons:\n"
                "• Video is unavailable or private\n"
                "• Network connection issue\n"
                "• Invalid format selected\n\n"
                "Please try again."
            )
            return

        base, ext = os.path.splitext(filepath)
        new_filepath = os.path.join(os.path.dirname(filepath), f"{new_filename}{ext}")
        os.rename(filepath, new_filepath)
        filepath = new_filepath

        await upload_and_send_file(client, user_id, filepath, new_filename, format_type, status_msg, message)

    except Exception as e:
        print(f"Download error: {e}")
        await status_msg.edit_text(f"❌ Error during download: {str(e)}")
        if 'filepath' in locals() and filepath:
            cleanup_file(filepath)

async def upload_and_send_file(client, user_id, filepath, title, format_type, status_msg, context):
    is_premium = await db.is_premium(user_id)
    max_size = Config.FREE_MAX_SIZE_MB if not is_premium else float('inf')

    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)

    if not is_premium and file_size_mb > max_size:
        cleanup_file(filepath)
        await status_msg.edit_text(
            f"❌ File too large ({int(file_size_mb)}MB)!\n\n"
            f"Your limit: {max_size}MB\n"
            "💎 Upgrade to Premium for unlimited file sizes with auto-split!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💎 Get Premium", callback_data="premium")
            ]])
        )
        return

    # Generate download link
    filename = os.path.basename(filepath)
    download_url = generate_download_link(filepath, filename)

    # Offer choice between Telegram upload and web download
    await status_msg.edit_text(
        f"✅ **File Ready!**\n\n"
        f"📁 {title}\n"
        f"💾 Size: {int(file_size_mb)}MB\n\n"
        f"Choose download method:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Fast Download (Web)", url=download_url)],
            [InlineKeyboardButton("📤 Upload to Telegram", callback_data=f"tg_upload_{user_id}")]
        ])
    )

    # Store filepath for later telegram upload if user chooses
    user_downloads[user_id]['ready_file'] = filepath
    user_downloads[user_id]['ready_title'] = title
    user_downloads[user_id]['ready_format_type'] = format_type

    return

    """Perform the actual Telegram upload"""
    status_msg = await status_msg.edit_text("📤 Uploading to Telegram...")

    is_premium = await db.is_premium(user_id)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Download thumbnail
    thumbnail_path = None
    if user_id in user_downloads and user_downloads[user_id].get('thumbnail'):
        thumbnail_url = user_downloads[user_id]['thumbnail']
        thumb_save_path = os.path.join(Config.DOWNLOAD_DIR, f"thumb_{user_id}.jpg")
        thumbnail_path = await download_thumbnail(thumbnail_url, thumb_save_path)
        if thumbnail_path and not os.path.exists(thumbnail_path):
            thumbnail_path = None

    caption = f"📁 **{title}**\n\n"
    caption += f"📊 Size: {int(file_size_mb)}MB\n"

    if hasattr(context, 'from_user'):
        caption += f"📥 Downloaded by: {context.from_user.first_name}"

    # Progress callback for upload
    upload_stats = {'last_update': 0, 'start_time': __import__('time').time()}

    async def upload_progress(current, total):
        import time
        now = time.time()
        if now - upload_stats['last_update'] >= 2:
            upload_stats['last_update'] = now
            try:
                percent = int((current / total) * 100) if total > 0 else 0
                speed = (current / (1024 * 1024)) / max(1, now - upload_stats['start_time'])
                eta_seconds = int((total - current) / max(1, current / max(1, now - upload_stats['start_time'])))

                progress_text = f"📥 Download: {create_progress_bar(100)} 100%\n"
                progress_text += f"📤 Upload:   {create_progress_bar(percent)} {percent}%\n\n"
                progress_text += f"💾 {int(current / (1024 * 1024))}MB / {int(total / (1024 * 1024))}MB | "
                progress_text += f"⚡ {speed:.1f}MB/s | ⏱ ETA: {format_eta(eta_seconds)}"

                await status_msg.edit_text(progress_text)
            except:
                pass

    if file_size_mb > Config.TELEGRAM_MAX_SIZE_MB:
        await status_msg.edit_text(f"📦 File is large ({int(file_size_mb)}MB). Splitting into parts...")

        parts = await split_file(filepath, Config.SPLIT_SIZE_MB)

        for idx, part_path in enumerate(parts, 1):
            part_caption = f"{caption}\n\n📦 Part {idx}/{len(parts)}"

            await status_msg.edit_text(f"📤 Uploading part {idx}/{len(parts)}...")

            # Reset upload progress timer for each part
            upload_stats['start_time'] = __import__('time').time()
            upload_stats['last_update'] = 0

            try:
                if format_type == 'audio':
                    sent_msg = await context.reply_audio(
                        audio=part_path,
                        caption=part_caption,
                        title=f"{title} - Part {idx}",
                        thumb=thumbnail_path,
                        progress=upload_progress
                    ) if hasattr(context, 'reply_audio') else await status_msg.reply_audio(
                        audio=part_path,
                        caption=part_caption,
                        title=f"{title} - Part {idx}",
                        thumb=thumbnail_path,
                        progress=upload_progress
                    )
                else:
                    if hasattr(context, 'reply_video'):
                        sent_msg = await context.reply_video(
                            video=part_path,
                            caption=part_caption,
                            supports_streaming=True,
                            thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                            progress=upload_progress
                        )
                    else:
                        sent_msg = await status_msg.reply_video(
                            video=part_path,
                            caption=part_caption,
                            supports_streaming=True,
                            thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                            progress=upload_progress
                        )

                try:
                    await client.copy_message(
                        chat_id=Config.STORAGE_CHANNEL_ID,
                        from_chat_id=sent_msg.chat.id,
                        message_id=sent_msg.id
                    )
                except Exception as e:
                    print(f"Failed to backup part {idx} to storage channel: {e}")

            except Exception as e:
                print(f"Error uploading part {idx}: {e}")

        await cleanup_parts(parts)
        cleanup_file(filepath)

    else:
        try:
            await status_msg.edit_text("📤 Sending file to Telegram...")
        except:
            pass  # Message might not be editable

        sent_msg = None
        try:
            if format_type == 'audio':
                sent_msg = await context.reply_audio(
                    audio=filepath,
                    caption=caption,
                    title=title,
                    thumb=thumbnail_path,
                    progress=upload_progress
                ) if hasattr(context, 'reply_audio') else await status_msg.reply_audio(
                    audio=filepath,
                    caption=caption,
                    title=title,
                    thumb=thumbnail_path,
                    progress=upload_progress
                )
            else:
                if hasattr(context, 'reply_video'):
                    sent_msg = await context.reply_video(
                        video=filepath,
                        caption=caption,
                        supports_streaming=True,
                        thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                        progress=upload_progress
                    )
                else:
                    sent_msg = await status_msg.reply_video(
                        video=filepath,
                        caption=caption,
                        supports_streaming=True,
                        thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                        progress=upload_progress
                    )

            # Only cleanup after successful upload to user
            cleanup_file(filepath)

            # Try to backup to storage channel (non-critical, can fail)
            if sent_msg:
                try:
                    await client.copy_message(
                        chat_id=Config.STORAGE_CHANNEL_ID,
                        from_chat_id=sent_msg.chat.id,
                        message_id=sent_msg.id
                    )
                except Exception as e:
                    print(f"Failed to backup to storage channel: {e}")

        except Exception as e:
            print(f"Error uploading file: {e}")
            cleanup_file(filepath)

    if thumbnail_path:
        cleanup_file(thumbnail_path)

    await db.increment_downloads(user_id)

    await status_msg.edit_text("✅ Download completed!")

    if user_id in user_downloads:
        del user_downloads[user_id]

@app.on_message(filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in user_downloads:
        del user_downloads[user_id]
        await message.reply_text("❌ Operation cancelled.")
    else:
        await message.reply_text("ℹ️ No active operation to cancel.")

@app.on_callback_query(filters.regex(r'^premium$'))
async def premium_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    await show_premium_page(callback_query.message)

@app.on_callback_query(filters.regex(r'^payment_qr$'))
async def payment_qr_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()

    if Config.PAYMENT_QR_IMAGE:
        try:
            await callback_query.message.reply_photo(
                photo=Config.PAYMENT_QR_IMAGE,
                caption="💳 **Payment QR Code**\n\n"
                "Scan this QR code to make payment.\n"
                "After payment, contact admin with proof for activation."
            )
        except:
            await callback_query.message.reply_text(
                "❌ QR image not available. Please contact admin directly."
            )
    else:
        await callback_query.message.reply_text(
            "❌ Payment QR not configured. Please contact admin."
        )

@app.on_callback_query(filters.regex(r'^help$'))
async def help_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    await help_command(client, callback_query.message)

@app.on_callback_query(filters.regex(r'^tg_upload_'))
async def telegram_upload_callback(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split('_')[2])

    if user_id != callback_query.from_user.id:
        await callback_query.answer("❌ This is not your download!", show_alert=True)
        return

    if user_id not in user_downloads or 'ready_file' not in user_downloads[user_id]:
        await callback_query.answer("❌ Session expired. Please start over.", show_alert=True)
        return

    await callback_query.answer("📤 Starting Telegram upload...")

    filepath = user_downloads[user_id]['ready_file']
    title = user_downloads[user_id]['ready_title']
    format_type = user_downloads[user_id]['ready_format_type']

    await perform_telegram_upload(client, user_id, filepath, title, format_type, callback_query.message, callback_query)

async def perform_telegram_upload(client, user_id, filepath, title, format_type, status_msg, context):
    """Perform the actual Telegram upload"""
    status_msg = await status_msg.edit_text("📤 Uploading to Telegram...")

    is_premium = await db.is_premium(user_id)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Download thumbnail
    thumbnail_path = None
    if user_id in user_downloads and user_downloads[user_id].get('thumbnail'):
        thumbnail_url = user_downloads[user_id]['thumbnail']
        thumb_save_path = os.path.join(Config.DOWNLOAD_DIR, f"thumb_{user_id}.jpg")
        thumbnail_path = await download_thumbnail(thumbnail_url, thumb_save_path)
        if thumbnail_path and not os.path.exists(thumbnail_path):
            thumbnail_path = None

    caption = f"📁 **{title}**\n\n"
    caption += f"📊 Size: {int(file_size_mb)}MB\n"

    if hasattr(context, 'from_user'):
        caption += f"📥 Downloaded by: {context.from_user.first_name}"

    # Progress callback for upload
    upload_stats = {'last_update': 0, 'start_time': __import__('time').time()}

    async def upload_progress(current, total):
        import time
        now = time.time()
        if now - upload_stats['last_update'] >= 2:
            upload_stats['last_update'] = now
            try:
                percent = int((current / total) * 100) if total > 0 else 0
                speed = (current / (1024 * 1024)) / max(1, now - upload_stats['start_time'])
                eta_seconds = int((total - current) / max(1, current / max(1, now - upload_stats['start_time'])))

                progress_text = f"📥 Download: {create_progress_bar(100)} 100%\n"
                progress_text += f"📤 Upload:   {create_progress_bar(percent)} {percent}%\n\n"
                progress_text += f"💾 {int(current / (1024 * 1024))}MB / {int(total / (1024 * 1024))}MB | "
                progress_text += f"⚡ {speed:.1f}MB/s | ⏱ ETA: {format_eta(eta_seconds)}"

                await status_msg.edit_text(progress_text)
            except:
                pass

    if file_size_mb > Config.TELEGRAM_MAX_SIZE_MB:
        await status_msg.edit_text(f"📦 File is large ({int(file_size_mb)}MB). Splitting into parts...")

        parts = await split_file(filepath, Config.SPLIT_SIZE_MB)

        for idx, part_path in enumerate(parts, 1):
            part_caption = f"{caption}\n\n📦 Part {idx}/{len(parts)}"

            await status_msg.edit_text(f"📤 Uploading part {idx}/{len(parts)}...")

            # Reset upload progress timer for each part
            upload_stats['start_time'] = __import__('time').time()
            upload_stats['last_update'] = 0

            try:
                if format_type == 'audio':
                    sent_msg = await context.reply_audio(
                        audio=part_path,
                        caption=part_caption,
                        title=f"{title} - Part {idx}",
                        thumb=thumbnail_path,
                        progress=upload_progress
                    ) if hasattr(context, 'reply_audio') else await status_msg.reply_audio(
                        audio=part_path,
                        caption=part_caption,
                        title=f"{title} - Part {idx}",
                        thumb=thumbnail_path,
                        progress=upload_progress
                    )
                else:
                    if hasattr(context, 'reply_video'):
                        sent_msg = await context.reply_video(
                            video=part_path,
                            caption=part_caption,
                            supports_streaming=True,
                            thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                            progress=upload_progress
                        )
                    else:
                        sent_msg = await status_msg.reply_video(
                            video=part_path,
                            caption=part_caption,
                            supports_streaming=True,
                            thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                            progress=upload_progress
                        )

                try:
                    await client.copy_message(
                        chat_id=Config.STORAGE_CHANNEL_ID,
                        from_chat_id=sent_msg.chat.id,
                        message_id=sent_msg.id
                    )
                except Exception as e:
                    print(f"Failed to backup part {idx} to storage channel: {e}")

            except Exception as e:
                print(f"Error uploading part {idx}: {e}")

        await cleanup_parts(parts)
        cleanup_file(filepath)

    else:
        try:
            await status_msg.edit_text("📤 Sending file to Telegram...")
        except:
            pass  # Message might not be editable

        sent_msg = None
        try:
            if format_type == 'audio':
                sent_msg = await context.reply_audio(
                    audio=filepath,
                    caption=caption,
                    title=title,
                    thumb=thumbnail_path,
                    progress=upload_progress
                ) if hasattr(context, 'reply_audio') else await status_msg.reply_audio(
                    audio=filepath,
                    caption=caption,
                    title=title,
                    thumb=thumbnail_path,
                    progress=upload_progress
                )
            else:
                if hasattr(context, 'reply_video'):
                    sent_msg = await context.reply_video(
                        video=filepath,
                        caption=caption,
                        supports_streaming=True,
                        thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                        progress=upload_progress
                    )
                else:
                    sent_msg = await status_msg.reply_video(
                        video=filepath,
                        caption=caption,
                        supports_streaming=True,
                        thumb=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                        progress=upload_progress
                    )

            cleanup_file(filepath)

            if sent_msg:
                try:
                    await client.copy_message(
                        chat_id=Config.STORAGE_CHANNEL_ID,
                        from_chat_id=sent_msg.chat.id,
                        message_id=sent_msg.id
                    )
                except Exception as e:
                    print(f"Failed to backup to storage channel: {e}")

        except Exception as e:
            print(f"Error uploading file: {e}")
            cleanup_file(filepath)

    if thumbnail_path:
        cleanup_file(thumbnail_path)

    await status_msg.edit_text("✅ Upload completed!")

    if user_id in user_downloads:
        del user_downloads[user_id]

if __name__ == "__main__":
    print("🚀 Starting Inert Downloader Bot...")
    print(f"📊 Database: {db.db_type.upper()}")
    print(f"💾 Storage Channel: {Config.STORAGE_CHANNEL_ID}")
    print(f"⚙️ Free Download Limit: {Config.FREE_DOWNLOAD_LIMIT}/day")

    # Start web preview server
    run_web_preview()
    print("🌐 Web preview running on port 5000")

    print("✅ Bot is running!")
    app.run()