"""
Inert Downloader Bot - File Splitter Module
Developer: @TheInertGuy
Updates: @Theinertbotz
Support: @Theinertbotzchart
"""

import os
import asyncio
from typing import List

async def split_file(filepath: str, split_size_mb: int = 1800) -> List[str]:
    split_size_bytes = split_size_mb * 1024 * 1024
    file_size = os.path.getsize(filepath)

    if file_size <= split_size_bytes:
        return [filepath]

    parts = []
    base_name = os.path.splitext(filepath)[0]
    ext = os.path.splitext(filepath)[1]

    part_num = 1

    loop = asyncio.get_event_loop()

    def _split():
        nonlocal part_num
        with open(filepath, 'rb') as source:
            while True:
                chunk = source.read(split_size_bytes)
                if not chunk:
                    break

                part_filename = f"{base_name}_part{part_num}{ext}"
                with open(part_filename, 'wb') as part_file:
                    part_file.write(chunk)

                parts.append(part_filename)
                part_num += 1

    await loop.run_in_executor(None, _split)

    return parts

async def cleanup_parts(parts: List[str]):
    for part in parts:
        try:
            if os.path.exists(part):
                os.remove(part)
        except Exception as e:
            print(f"Error cleaning up part {part}: {e}")