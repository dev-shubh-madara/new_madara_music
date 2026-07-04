# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  The Most Powerful Telegram Music Bot            ║
# ║  Built with ❤️ for music lovers everywhere       ║
# ╚══════════════════════════════════════════════════╝
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from MADARAMUSIC import app
from MADARAMUSIC.core.call import MADARA
from MADARAMUSIC.utils import bot_sys_stats
from MADARAMUSIC.utils.decorators.language import language
from MADARAMUSIC.utils.inline import supp_markup
from config import BANNED_USERS, MADARA_IMG
import random


@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    # ── Radha Music header ─────────────────────────────────────────
    header = (
        "<code>ʀᴀᴅʜᴀ ᴍᴜsɪᴄ</code>\n\n"
        f"⚡ {app.mention} ɪs ᴘɪɴɢɪɴɢ... 🎵"
    )
    response = await message.reply_photo(
        random.choice(MADARA_IMG),
        caption=header,
    )

    pytgping = await MADARA.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    # ── Full ping result with Powered by Madara ────────────────────
    ping_text = (
        "<code>ʀᴀᴅʜᴀ ᴍᴜsɪᴄ</code>\n\n"
        "<b>╔══════════════════╗\n"
        "🎵 𝗠𝗔𝗗𝗔𝗥𝗔 𝗠𝗨𝗦𝗜𝗖 𝗣𝗜𝗡𝗚\n"
        "╚══════════════════╝</b>\n\n"
        f"⚡ ᴘɪɴɢ : <code>{resp}ᴍs</code>\n\n"
        f"<u>📊 {app.mention} sᴛᴀᴛɪsᴛɪᴄs :</u>\n"
        f"🕛 ᴜᴩᴛɪᴍᴇ : {UP}\n"
        f"💾 ʀᴀᴍ : {RAM}\n"
        f"💻 ᴄᴩᴜ : {CPU}\n"
        f"💿 ᴅɪsᴋ : {DISK}\n"
        f"📡 ᴩʏ-ᴛɢᴄᴀʟʟs : <code>{pytgping}ᴍs</code>\n\n"
        "<code>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴍᴀᴅᴀʀᴀ</code>"
    )

    await response.edit_caption(
        caption=ping_text,
        reply_markup=supp_markup(_),
    )
