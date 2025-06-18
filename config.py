import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

#Get API_KEY from @Nikchil
API_BASE_URL = getenv("API_BASE_URL", "")
API_KEY = getenv("API_KEY")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 9999))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @Harry_RoxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 7967798005))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/GrayBots/AudifyMusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/GrayBots")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/GrayBotSupport")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 9999))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/7a5bdfcf40189ea450ed0-c1fd755b77e93c2d7a.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org//file/389a372e8ae039320ca6c.png"
)
PLAYLIST_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
STATS_IMG_URL = "https://graph.org/file/cf84606db2e13b5cb19cc-2b375f36e4dcec4055.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
STREAM_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
