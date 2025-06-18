

# ==========================================================
# 🎧 Public Open-Source VC Player Music Bot (Cookies Based)
# 🛠️ Maintained by Team GrayBots | Lead Developer: @Nikchil
# 🔓 Licensed for Public Use — All Rights Reserved © Team GrayBots
#
# This file is part of a publicly available and open-source Telegram music bot
# developed by Team GrayBots. It offers high-quality streaming in Telegram voice
# chats using YouTube as a source, supported by session-based assistant accounts and
# YouTube cookie integration for improved access and performance.
#
# 💡 This source code is released for educational and community purposes. You're free
# to study, modify, and deploy it under fair and respectful usage. However, any misuse,
# removal of credits, or false ownership claims will be considered a violation of our
# community standards and may lead to denial of support or blacklisting.
#
# 🔗 Looking for powerful performance with stable APIs? Get access to the official
# Get Your API from @Nikchil
#
# ❤️ Openly built for the community, but proudly protected by the passion of its creators.
# ==========================================================




from os import path

from yt_dlp import YoutubeDL

from GrayBots.utils.formatters import seconds_to_min


class SoundAPI:
    def __init__(self):
        self.opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "best",
            "retries": 3,
            "nooverwrites": False,
            "continuedl": True,
        }

    async def valid(self, link: str):
        if "soundcloud" in link:
            return True
        else:
            return False

    async def download(self, url):
        d = YoutubeDL(self.opts)
        try:
            info = d.extract_info(url)
        except:
            return False
        xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
        duration_min = seconds_to_min(info["duration"])
        track_details = {
            "title": info["title"],
            "duration_sec": info["duration"],
            "duration_min": duration_min,
            "uploader": info["uploader"],
            "filepath": xyz,
        }
        return track_details, xyz
