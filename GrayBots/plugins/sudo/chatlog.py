import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from GrayBots import app
from config import LOGGER_ID as JOINLOGS

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Cache the bot's ID at startup
BOT_ID = None


@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    global BOT_ID

    try:
        if BOT_ID is None:
            bot_user = await client.get_me()
            BOT_ID = bot_user.id
            logger.info(f"Cached bot ID: {BOT_ID}")
    except Exception as e:
        logger.exception("Failed to get bot info")
        return  # Early exit to prevent further failures

    for new_member in message.new_chat_members:
        if new_member.id == BOT_ID:
            try:
                added_by = (
                    f"<a href='tg://user?id={message.from_user.id}'>👤{message.from_user.first_name}</a>"
                    if message.from_user else "Unknown User"
                )

                chat_title = message.chat.title
                chat_id = message.chat.id
                chat_username = f"@{message.chat.username}" if message.chat.username else "Private Group"
                chat_link = (
                    f"https://t.me/{message.chat.username}"
                    if message.chat.username else None
                )

                log_text = (
                    "<b>🚀 Bot Added Successfully!</b>\n\n"
                    "╭───────⍟\n"
                    f"├ 💬 <b>Chat Name:</b> <code>{chat_title}</code>\n"
                    f"├ 🆔 <b>Chat ID:</b> <code>{chat_id}</code>\n"
                    f"├ 🌐 <b>Username:</b> {chat_username}\n"
                    f"└ 👤 <b>Added By:</b> {added_by}\n"
                    "╰─────────────⍟"
                )

                buttons = [[InlineKeyboardButton("➤ Link 🔗", url=chat_link)]] if chat_link else None

                await client.send_message(
                    JOINLOGS,
                    text=log_text,
                    reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                    disable_web_page_preview=True
                )
                logger.info(f"Join log sent for chat ID: {chat_id}")
            except Exception as e:
                logger.exception(f"[JOINLOG ERROR] Failed to send join log for chat ID: {message.chat.id}")


