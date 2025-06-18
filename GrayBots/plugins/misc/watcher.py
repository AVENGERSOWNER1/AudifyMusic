# Powered By Team GrayBots

from pyrogram import filters
from pyrogram.types import Message

from GrayBots import app
from GrayBots.core.call import Audify

welcome = 20
close = 30


@app.on_message(filters.video_chat_started, group=welcome)
@app.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await Audify.stop_stream_force(message.chat.id)
