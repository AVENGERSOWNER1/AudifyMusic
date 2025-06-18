import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message
from GrayBots import app
from GrayBots.misc import SUDOERS
from GrayBots.utils.decorators.language import language


def perform_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        st.results.share()
        return st.results.dict()
    except Exception as e:
        return {"error": str(e)}


@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, _):
    status = await message.reply_text("⚡ <b>Running SpeedTest...</b>\nConnecting to best server...")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, perform_speedtest)

    if "error" in result:
        return await status.edit_text(f"❌ <b>Speedtest failed</b>\n<code>{result['error']}</code>")

    download_speed = round(result['download'] / 1_000_000, 2)
    upload_speed = round(result['upload'] / 1_000_000, 2)

    output = (
        "<b>🌐 SpeedTest Results</b>\n\n"
        f"🧑 <b>ISP:</b> <code>{result['client']['isp']}</code>\n"
        f"🌍 <b>Country:</b> <code>{result['client']['country']}</code>\n\n"
        f"🏢 <b>Server:</b> <code>{result['server']['name']} ({result['server']['country']} - {result['server']['cc']})</code>\n"
        f"🤝 <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>\n"
        f"⏱ <b>Latency:</b> <code>{round(result['server']['latency'], 2)} ms</code>\n"
        f"📶 <b>Ping:</b> <code>{result['ping']} ms</code>\n\n"
        f"⬇️ <b>Download:</b> <code>{download_speed} Mbps</code>\n"
        f"⬆️ <b>Upload:</b> <code>{upload_speed} Mbps</code>\n"
    )

    try:
        await client.send_photo(message.chat.id, photo=result["share"], caption=output)
    except Exception:
        await status.edit_text(output)
    else:
        await status.delete()
