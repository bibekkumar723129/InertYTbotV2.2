"""
Inert Downloader Bot - YouTube Downloader Module
Developer: @TheInertGuy
Updates: @Theinertbotz
Support: @Theinertbotzchart
"""

import os
import asyncio
import yt_dlp
from typing import Dict, List, Optional, Any
from config import Config

class Downloader:
    def __init__(self):
        self.download_dir = Config.DOWNLOAD_DIR

    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                None,
                lambda: self._extract_info(url, ydl_opts)
            )

            return info
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def _extract_info(self, url: str, ydl_opts: dict):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    async def get_available_formats(self, url: str) -> List[Dict[str, Any]]:
        info = await self.get_video_info(url)
        if not info:
            return []

        formats = []
        seen_qualities = set()

        if 'formats' in info:
            for f in info['formats']:
                ext = f.get('ext', 'unknown')
                height = f.get('height', 0)
                format_id = f.get('format_id', '')
                filesize = f.get('filesize', 0) or f.get('filesize_approx', 0)

                if ext in ['mp4', 'webm'] and height and height >= 144:
                    quality = f"{height}p"
                    if quality not in seen_qualities:
                        seen_qualities.add(quality)
                        formats.append({
                            'format_id': format_id,
                            'quality': quality,
                            'ext': ext,
                            'filesize': filesize,
                            'type': 'video'
                        })

        audio_format = None
        for f in info.get('formats', []):
            if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                audio_format = {
                    'format_id': f.get('format_id', 'bestaudio'),
                    'quality': 'Audio Only',
                    'ext': f.get('ext', 'mp3'),
                    'filesize': f.get('filesize', 0) or f.get('filesize_approx', 0),
                    'type': 'audio'
                }
                break

        if not audio_format:
            audio_format = {
                'format_id': 'bestaudio',
                'quality': 'Audio Only',
                'ext': 'mp3',
                'filesize': 0,
                'type': 'audio'
            }

        formats.append(audio_format)

        formats.sort(key=lambda x: int(x['quality'].replace('p', '')) if x['quality'] != 'Audio Only' else 0)

        return formats

    async def download_media(
        self, 
        url: str, 
        format_id: str = 'best',
        progress_callback=None,
        format_type: str = 'video'
    ) -> Optional[str]:
        try:
            output_template = os.path.join(self.download_dir, '%(title)s.%(ext)s')

            if format_type == 'audio':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_template,
                    'quiet': False,
                    'no_warnings': False,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'prefer_ffmpeg': True,
                }
            else:
                ydl_opts = {
                    'format': format_id,
                    'outtmpl': output_template,
                    'quiet': False,
                    'no_warnings': False,
                }

            if progress_callback:
                ydl_opts['progress_hooks'] = [progress_callback]

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._download(url, ydl_opts)
            )

            if result and os.path.exists(result):
                print(f"✅ Download successful: {result}")
                return result
            else:
                print(f"❌ Download failed: File not found at {result}")
                return None

        except Exception as e:
            print(f"❌ Download error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _download(self, url: str, ydl_opts: dict):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if ydl_opts.get('postprocessors'):
                base, ext = os.path.splitext(filename)
                filename = base + '.mp3'

            return filename

downloader = Downloader()