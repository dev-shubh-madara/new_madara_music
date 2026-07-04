# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  The Most Powerful Telegram Music Bot            ║
# ║  Built with ❤️ for music lovers everywhere       ║
# ╚══════════════════════════════════════════════════╝
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MADARAMUSIC import app
from MADARAMUSIC.utils.database import get_lang, set_lang
from MADARAMUSIC.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string, languages_present


def lanuages_keyboard(_):
    """Build a language selection keyboard (2 per row)."""
    buttons = [
        InlineKeyboardButton(
            text=languages_present[i],
            callback_data=f"languages:{i}",
        )
        for i in languages_present
    ]
    # Arrange in rows of 2
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    rows.append([
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    ])
    return InlineKeyboardMarkup(rows)


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"],
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except Exception:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(_["lang_4"], show_alert=True)
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)
    except Exception:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
