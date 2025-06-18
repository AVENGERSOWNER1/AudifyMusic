

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


import uvloop
uvloop.install()

import asyncio
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Audify(Client):
    def __init__(self):
        LOGGER(__name__).info("🛠️ Initializing GrayBots Bot...")
        super().__init__(
            name="GrayBots",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<b>✅ Bot Started Successfully!</b>\n\n"
                    f"<b>Name:</b> {self.name}\n"
                    f"<b>Username:</b> @{self.username}\n"
                    f"<b>User ID:</b> <code>{self.id}</code>"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "❌ Unable to send message to the log group/channel. "
                "Ensure the bot is added and not banned."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"❌ Failed to access the log group/channel.\nReason: {type(ex).__name__}"
            )
            exit()

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "⚠️ Bot is not an admin in the log group/channel. Please promote it as admin."
                )
                exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"❌ Failed to fetch bot status in log group. Reason: {type(ex).__name__}"
            )
            exit()

        LOGGER(__name__).info(f"🎶 Bot is online and ready as {self.name} (@{self.username})")

    async def stop(self):
        LOGGER(__name__).info("🛑 Stopping GrayBots Bot...")
        await super().stop()
