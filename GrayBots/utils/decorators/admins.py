import logging
from datetime import datetime
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from GrayBots import app
from GrayBots.misc import SUDOERS, db
from GrayBots.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
)
from config import SUPPORT_CHAT, adminlist, confirmer, LOGGER_ID as LOG_CHANNEL_ID
from strings import get_string
from ..formatters import int_to_alpha

logger = logging.getLogger(__name__)


async def log_admin_action(chat_id, user_id, reason, action=None):
    msg = (
        f"🚫 <b>Admin Blocked</b>\n"
        f"<b>Chat:</b> <code>{chat_id}</code>\n"
        f"<b>User:</b> <code>{user_id}</code>\n"
        f"<b>Action:</b> <code>{action or 'Unknown'}</code>\n"
        f"<b>Reason:</b> {reason}\n"
        f"<b>Time:</b> <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"
    )
    logger.warning(msg.replace("<b>", "").replace("</b>", ""))
    try:
        await app.send_message(LOG_CHANNEL_ID, msg)
    except Exception as e:
        logger.warning(f"Failed to send log to channel: {e}")

def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        try:
            if not await is_maintenance():
                if message.from_user.id not in SUDOERS:
                    await log_admin_action(message.chat.id, message.from_user.id, "Bot under maintenance", message.command[0])
                    return await message.reply_text(
                        text=f"{app.mention} is under maintenance. Visit <a href={SUPPORT_CHAT}>Support Chat</a> for more info.",
                        disable_web_page_preview=True,
                    )

            try:
                await message.delete()
            except Exception as e:
                logger.warning(f"Failed to delete message: {e}")

            try:
                lang_code = await get_lang(message.chat.id)
                _ = get_string(lang_code)
            except:
                _ = get_string("en")

            if message.sender_chat:
                await log_admin_action(message.chat.id, message.from_user.id, "Message sent from sender_chat")
                return await message.reply_text(
                    _["general_3"],
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("How to fix?", callback_data="AudifymousAdmin")]
                    ]),
                )

            if message.command[0].startswith("c"):
                chat_id = await get_cmode(message.chat.id)
                if not chat_id:
                    return await message.reply_text(_["setting_7"])
                try:
                    await app.get_chat(chat_id)
                except:
                    return await message.reply_text(_["cplay_4"])
            else:
                chat_id = message.chat.id

            if not await is_active_chat(chat_id):
                await log_admin_action(chat_id, message.from_user.id, "Chat is not active", message.command[0])
                return await message.reply_text(_["general_5"])

            if not await is_nonadmin_chat(message.chat.id):
                if message.from_user.id not in SUDOERS:
                    admins = adminlist.get(message.chat.id)
                    if not admins or message.from_user.id not in admins:
                        if await is_skipmode(message.chat.id):
                            upvote = await get_upvote_count(chat_id)
                            command = message.command[0].lstrip("c").lower()

                            if command == "speed":
                                await log_admin_action(chat_id, message.from_user.id, "Tried /speed in skipmode", command)
                                return await message.reply_text(_["admin_14"])

                            vote_markup = InlineKeyboardMarkup([
                                [InlineKeyboardButton("Vote", callback_data=f"ADMIN UpVote|{chat_id}_{command.title()}")]
                            ])

                            if chat_id not in confirmer:
                                confirmer[chat_id] = {}

                            try:
                                track = db[chat_id][0]
                                vidid = track.get("vidid")
                                file = track.get("file")
                            except Exception as e:
                                logger.error(f"Error fetching track data: {e}")
                                await log_admin_action(chat_id, message.from_user.id, "No track data", command)
                                return await message.reply_text(_["admin_14"])

                            info_msg = await message.reply_text(
                                f"<b>Admin Rights Needed</b>\n\n"
                                f"Refresh admin cache: /reload\n\n"
                                f"» {upvote} votes needed for this action.",
                                reply_markup=vote_markup
                            )
                            confirmer[chat_id][info_msg.id] = {"vidid": vidid, "file": file}
                            return
                        else:
                            await log_admin_action(chat_id, message.from_user.id, "Blocked: not admin + no skipmode", message.command[0])
                            return await message.reply_text(_["admin_14"])

            return await mystic(client, message, _, chat_id)

        except Exception as e:
            logger.exception(f"Unhandled exception in AdminRightsCheck: {e}")
            return await message.reply_text("⚠️ An internal error occurred.")
    return wrapper

def AdminActual(mystic):
    async def wrapper(client, message):
        try:
            if not await is_maintenance():
                if message.from_user.id not in SUDOERS:
                    await log_admin_action(message.chat.id, message.from_user.id, "Maintenance mode", "unknown")
                    return await message.reply_text(
                        text=f"{app.mention} is under maintenance. Visit <a href={SUPPORT_CHAT}>Support Chat</a> for more info.",
                        disable_web_page_preview=True,
                    )

            try:
                await message.delete()
            except:
                pass

            try:
                lang_code = await get_lang(message.chat.id)
                _ = get_string(lang_code)
            except:
                _ = get_string("en")

            if message.sender_chat:
                await log_admin_action(message.chat.id, message.from_user.id, "sender_chat")
                return await message.reply_text(
                    _["general_3"],
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("How to fix?", callback_data="AudifymousAdmin")]
                    ])
                )

            if message.from_user.id not in SUDOERS:
                try:
                    member = await app.get_chat_member(message.chat.id, message.from_user.id)
                    if not member.privileges or not member.privileges.can_manage_video_chats:
                        await log_admin_action(message.chat.id, message.from_user.id, "No permission to manage video chats")
                        return await message.reply_text(_["general_4"])
                except:
                    await log_admin_action(message.chat.id, message.from_user.id, "Error fetching member privileges")
                    return await message.reply_text(_["general_4"])

            return await mystic(client, message, _)
        except Exception as e:
            logger.exception(f"Unhandled error in AdminActual: {e}")
            return await message.reply_text("⚠️ An internal error occurred.")
    return wrapper

def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        try:
            if not await is_maintenance():
                if CallbackQuery.from_user.id not in SUDOERS:
                    await log_admin_action(CallbackQuery.message.chat.id, CallbackQuery.from_user.id, "Maintenance on CB", CallbackQuery.data)
                    return await CallbackQuery.answer(
                        f"{app.mention} is under maintenance. Visit Support Chat for more info.",
                        show_alert=True,
                    )

            try:
                lang_code = await get_lang(CallbackQuery.message.chat.id)
                _ = get_string(lang_code)
            except:
                _ = get_string("en")

            if CallbackQuery.message.chat.type == ChatType.PRIVATE:
                return await mystic(client, CallbackQuery, _)

            if not await is_nonadmin_chat(CallbackQuery.message.chat.id):
                try:
                    privileges = (
                        await app.get_chat_member(
                            CallbackQuery.message.chat.id,
                            CallbackQuery.from_user.id
                        )
                    ).privileges
                    if not privileges or not privileges.can_manage_video_chats:
                        if CallbackQuery.from_user.id not in SUDOERS:
                            token = await int_to_alpha(CallbackQuery.from_user.id)
                            if token not in await get_authuser_names(CallbackQuery.from_user.id):
                                await log_admin_action(CallbackQuery.message.chat.id, CallbackQuery.from_user.id, "No CB admin rights", CallbackQuery.data)
                                return await CallbackQuery.answer(_["general_4"], show_alert=True)
                except:
                    await log_admin_action(CallbackQuery.message.chat.id, CallbackQuery.from_user.id, "Error fetching CB member")
                    return await CallbackQuery.answer(_["general_4"], show_alert=True)

            return await mystic(client, CallbackQuery, _)
        except Exception as e:
            logger.exception(f"Error in ActualAdminCB: {e}")
            return await CallbackQuery.answer("⚠️ An error occurred", show_alert=True)
    return wrapper
