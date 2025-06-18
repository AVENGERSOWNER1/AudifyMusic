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


import os

from ..logging import LOGGER


def dirr():
    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)
        elif file.endswith(".jpeg"):
            os.remove(file)
        elif file.endswith(".png"):
            os.remove(file)

    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    if "cache" not in os.listdir():
        os.mkdir("cache")

    LOGGER(__name__).info("✔ Directory structure successfully updated.")
