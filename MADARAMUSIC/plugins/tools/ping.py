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
        "<tg-emoji emoji-id="5211009581727107238">R</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji><tg-emoji emoji-id="5211094355791594395">D</tg-emoji><tg-emoji emoji-id="5213415326053582248">H</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji> <tg-emoji emoji-id="5210890482283988215">M</tg-emoji><tg-emoji emoji-id="5213277251444952289">U</tg-emoji><tg-emoji emoji-id="5212928963956983272">S</tg-emoji><tg-emoji emoji-id="5211032856154885824">I</tg-emoji><tg-emoji emoji-id="5210687171417097576">C</tg-emoji>\n\n"
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
        "<tg-emoji emoji-id="5211009581727107238">R</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji><tg-emoji emoji-id="5211094355791594395">D</tg-emoji><tg-emoji emoji-id="5213415326053582248">H</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji> <tg-emoji emoji-id="5210890482283988215">M</tg-emoji><tg-emoji emoji-id="5213277251444952289">U</tg-emoji><tg-emoji emoji-id="5212928963956983272">S</tg-emoji><tg-emoji emoji-id="5211032856154885824">I</tg-emoji><tg-emoji emoji-id="5210687171417097576">C</tg-emoji>\n\n"
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
        "<tg-emoji emoji-id="5213095308040356426">P</tg-emoji><tg-emoji emoji-id="5212943085809454431">O</tg-emoji><tg-emoji emoji-id="5213148466850580086">W</tg-emoji><tg-emoji emoji-id="5213337333742454261">E</tg-emoji><tg-emoji emoji-id="5211009581727107238">R</tg-emoji><tg-emoji emoji-id="5213337333742454261">E</tg-emoji><tg-emoji emoji-id="5211094355791594395">D</tg-emoji> <tg-emoji emoji-id="5213400521301313365">B</tg-emoji><tg-emoji emoji-id="5210932667452768696">Y</tg-emoji> <tg-emoji emoji-id="5210890482283988215">M</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji><tg-emoji emoji-id="5211094355791594395">D</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji><tg-emoji emoji-id="5211009581727107238">R</tg-emoji><tg-emoji emoji-id="5210820276748566172">A</tg-emoji>"
    )

    await response.edit_caption(
        caption=ping_text,
        reply_markup=supp_markup(_),
    )
