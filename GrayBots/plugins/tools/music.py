# ==========================================================
# 🔒 All Rights Reserved © Team GrayBots
# 📁 This file is part of the GrayBots Project.
# ==========================================================


import os
import re
import asyncio
import requests
import logging
import urllib.request
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatAction
from youtubesearchpython.__future__ import VideosSearch
from config import API_KEY, API_BASE_URL
from GrayBots import app

# 📝 Logging Setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("logs/music_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MIN_FILE_SIZE = 51200
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def extract_video_id(link: str) -> str | None:
    patterns = [
        r'youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None

def download_thumbnail(video_id: str) -> str | None:
    try:
        url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        path = os.path.join(DOWNLOADS_DIR, f"{video_id}.jpg")
        urllib.request.urlretrieve(url, path)
        return path
    except Exception as e:
        logger.warning(f"Thumbnail error: {e}")
        return None

def api_dl(video_id: str) -> str | None:
    try:
        url = f"{API_BASE_URL}/download/song/{video_id}?key={API_KEY}"
        file_path = os.path.join(DOWNLOADS_DIR, f"{video_id}.mp3")
        if os.path.exists(file_path):
            return file_path
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(file_path) < MIN_FILE_SIZE:
                os.remove(file_path)
                return None
            return file_path
    except Exception as e:
        logger.error(f"Download failed: {e}")
    return None

def parse_duration(duration: str) -> int:
    parts = list(map(int, duration.split(":")))
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m = 0, parts[0]
        s = parts[1]
    else:
        return int(parts[0])
    return h * 3600 + m * 60 + s

@app.on_message(filters.command(["song", "music"]))
async def song_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🎧 <b>𝖴𝗌𝖺𝗀𝖾:</b> <code>/music [song name or YouTube link]</code>")

    query = message.text.split(None, 1)[1].strip()
    video_id = extract_video_id(query)

    if video_id:
        msg = await message.reply_text("🎼 𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝗍𝗋𝖺𝖼𝗄...")
        await send_audio(client, msg, video_id)
    else:
        try:
            results = (await VideosSearch(query, limit=5).next()).get('result', [])
            if not results:
                return await message.reply_text("❌ 𝖭𝗈 𝗌𝗈𝗇𝗀𝗌 𝖿𝗈𝗎𝗇𝖽.")
            buttons = [[
                InlineKeyboardButton(f"🎙 {video['title'][:30]}{'...' if len(video['title']) > 30 else ''}",
                                     callback_data=f"dl_{video['id']}")
            ] for video in results]
            await message.reply_text(
                "🎧 𝖲𝖾𝗅𝖾𝖼𝗍 𝖺 𝗌𝗈𝗇𝗀:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            logger.error(f"Search error: {e}")
            await message.reply_text("⚠️ 𝖤𝗋𝗋𝗈𝗋 𝗐𝗁𝗂𝗅𝖾 𝗌𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀.")

@app.on_callback_query(filters.regex(r"^dl_(.+)$"))
async def callback_handler(client: Client, cq: CallbackQuery):
    video_id = cq.data.split("_", 1)[1]
    await cq.answer()
    await cq.message.edit("⏳ 𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀 𝗍𝗋𝖺𝖼𝗄...")
    await send_audio(client, cq.message, video_id)

async def send_audio(client: Client, message: Message, video_id: str):
    try:
        result = (await VideosSearch(video_id, limit=1).next())["result"][0]
        title = result.get("title", "Unknown")
        duration_str = result.get("duration", "0:00")
        duration = parse_duration(duration_str)
        url = result.get("link")
    except Exception as e:
        logger.warning(f"Metadata error: {e}")
        title, duration_str, duration, url = "Unknown", "0:00", 0, None

    thumb_path = await asyncio.to_thread(download_thumbnail, video_id)
    file_path = await asyncio.to_thread(api_dl, video_id)

    if not file_path:
        return await message.edit("❌ 𝖢𝗈𝗎𝗅𝖽𝗇’𝗍 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗍𝗁𝖾 𝗌𝗈𝗇𝗀.")

    await message.edit("🎶 𝖲𝖾𝗇𝖽𝗂𝗇𝗀 𝗍𝗋𝖺𝖼𝗄...")

    await message.reply_audio(
        audio=file_path,
        title=title,
        performer="GrayBots",
        duration=duration,
        caption=f"📻 <b><a href=\"{url}\">{title}</a></b>\n🕒 <b>Duration:</b> {duration_str}\n🔧 <b>Powered by:</b> <a href=\"https://t.me/GrayBots\">GrayBots</a>",
        thumb=thumb_path if thumb_path else None,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💻 Source", url="https://github.com/GrayBots/AudifyMusic")]
        ])
    )
