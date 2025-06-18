from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from GrayBots import app
from GrayBots.misc import SUDOERS
from GrayBots.utils.database import get_client, is_active_chat
from config import LOGGER_ID
from pyrogram.enums import ChatType

from GrayBots.core.userbot import assistants


async def clean_assistant_chats(client, assistant_num):
    total_left = 0
    try:
        userbot = await get_client(assistant_num)
        left = 0
        async for dialog in userbot.get_dialogs():
            chat = dialog.chat
            if chat.type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
                if chat.id in [LOGGER_ID, -1001686672798, -1001549206010]:  # Excluded chats
                    continue
                if not await is_active_chat(chat.id):
                    try:
                        await userbot.leave_chat(chat.id)
                        left += 1
                    except Exception as e:
                        print(f"[CleanAssistant Error] Failed to leave {chat.title} ({chat.id}): {e}")
        total_left += left
    except Exception as e:
        print(f"[CleanAssistant Error] Assistant {assistant_num} failed: {e}")

    return total_left


@app.on_message(filters.command("cleanassistants") & filters.private & SUDOERS )
async def clean_assistants_command(client, message: Message):
    args = message.text.split()
    if len(args) == 1:
        # No assistant id given, show buttons + clean all
        buttons = [
            [InlineKeyboardButton(f"Assistant {num}", callback_data=f"clean_assistant:{num}")]
            for num in assistants
        ]
        # Add Clean All button at the bottom
        buttons.append([InlineKeyboardButton("Clean All Assistants 🧹", callback_data="clean_assistant:all")])

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            "Select the assistant to clean inactive chats, or clean all assistants:",
            reply_markup=reply_markup,
        )
    else:
        # assistant id given
        arg = args[1].lower()
        if arg == "all":
            msg = await message.reply_text(f"🧹 Cleaning all assistants... Please wait.")
            total_left_all = 0
            for assistant_id in assistants:
                total_left_all += await clean_assistant_chats(client, assistant_id)
            await msg.edit_text(f"✅ Cleaned all assistants.\nTotal chats left: <b>{total_left_all}</b>.")
        else:
            try:
                assistant_id = int(arg)
            except ValueError:
                return await message.reply_text("Invalid assistant id. Please provide a number or 'all'.")

            if assistant_id not in assistants:
                return await message.reply_text("This assistant id is not valid or not available.")

            msg = await message.reply_text(f"🧹 Cleaning inactive chats for assistant {assistant_id}... Please wait.")
            total_left = await clean_assistant_chats(client, assistant_id)
            await msg.edit_text(f"✅ Cleaned assistant {assistant_id}.\nTotal chats left: <b>{total_left}</b>.")


@app.on_callback_query(filters.regex(r"^clean_assistant:(all|\d+)$"))
async def clean_assistant_callback(client, callback_query: CallbackQuery):
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("You are not authorized.", show_alert=True)

    arg = callback_query.data.split(":")[1]
    if arg == "all":
        await callback_query.answer("Cleaning all assistants...")
        msg = await callback_query.message.edit_text(f"🧹 Cleaning all assistants... Please wait.")
        total_left_all = 0
        for assistant_id in assistants:
            total_left_all += await clean_assistant_chats(client, assistant_id)
        await msg.edit_text(f"✅ Cleaned all assistants.\nTotal chats left: <b>{total_left_all}</b>.")
    else:
        assistant_id = int(arg)
        if assistant_id not in assistants:
            return await callback_query.answer("Invalid assistant id.", show_alert=True)

        await callback_query.answer("Cleaning started...")
        msg = await callback_query.message.edit_text(f"🧹 Cleaning inactive chats for assistant {assistant_id}... Please wait.")
        total_left = await clean_assistant_chats(client, assistant_id)
        await msg.edit_text(f"✅ Cleaned assistant {assistant_id}.\nTotal chats left: <b>{total_left}</b>.")
