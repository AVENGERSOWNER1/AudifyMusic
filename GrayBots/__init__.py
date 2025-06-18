# Powered By Team GrayBots
from GrayBots.core.bot import Audify
from GrayBots.core.dir import dirr
from GrayBots.core.git import git
from GrayBots.core.userbot import Userbot
from GrayBots.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Audify()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
