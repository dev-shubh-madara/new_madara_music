import asyncio
import random
import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch
import config
from MADARAMUSIC import app
from MADARAMUSIC.misc import _boot_
from MADARAMUSIC.plugins.sudo.sudoers import sudoers_list
from MADARAMUSIC.utils import bot_sys_stats
from MADARAMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from MADARAMUSIC.utils.decorators.language import LanguageStart
from MADARAMUSIC.utils.formatters import get_readable_time
from MADARAMUSIC.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string
from config import BANNED_USERS, MADARA_IMG
from MADARAMUSIC.core.mongo import mongodb as _db

# ── Custom welcome DB ────────────────────────────────────────────
_welcome_db = _db.welcome_config

EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]

GREET = ["💞", "🥂", "🔍", "🧪", "⚡️", "🔥", "🎵"]


# ── Welcome helpers ──────────────────────────────────────────────
async def _get_caption(msg_type: str, default: str, user, bot, chat=None) -> str:
    data = await _welcome_db.find_one({"_id": msg_type})
    if data and "message" in data:
        text = data["message"]
        text = text.replace("{name}", user.first_name or "")
        text = text.replace("{mention}", user.mention or user.first_name)
        text = text.replace("{username}", f"@{user.username}" if user.username else "No Username")
        text = text.replace("{bot_name}", bot.first_name)
        if chat:
            text = text.replace("{chat_name}", chat.title or "")
        return text
    return default


# ── /setwelcome_dm and /setwelcome_grp (owner only) ─────────────
@app.on_message(filters.command(["setwelcome_dm", "setwelcome_grp"]) & filters.user(config.OWNER_ID))
async def set_welcome_msg(client, message: Message):
    cmd = message.command[0].lower()
    msg_type = "welcome_dm" if "dm" in cmd else "welcome_group"

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            f"❌ <b>Usage:</b>\n<code>/{cmd} [HTML Message]</code>\n\n"
            "<b>Variables:</b> <code>{name}</code> · <code>{mention}</code> · "
            "<code>{username}</code> · <code>{bot_name}</code> · <code>{chat_name}</code>"
        )
    try:
        if message.reply_to_message:
            new_msg = (message.reply_to_message.text or message.reply_to_message.caption).html
        else:
            new_msg = message.text.html.split(None, 1)[1]
    except (IndexError, AttributeError):
        return await message.reply_text("❌ Could not extract text. Please try again.")

    await _welcome_db.update_one({"_id": msg_type}, {"$set": {"message": new_msg}}, upsert=True)
    await message.reply_text(f"✅ <b>{msg_type.replace('_', ' ').upper()} message set!</b>")


@app.on_message(filters.command(["resetwelcome"]) & filters.user(config.OWNER_ID))
async def reset_welcome_msg(client, message: Message):
    args = message.command
    msg_type = "welcome_group" if len(args) > 1 and args[1].lower() in ("grp", "group") else "welcome_dm"
    result = await _welcome_db.delete_one({"_id": msg_type})
    if result.deleted_count:
        await message.reply_text(f"✅ <b>{msg_type.replace('_', ' ').upper()} reset to default!</b>")
    else:
        await message.reply_text(f"ℹ️ No custom {msg_type.replace('_', ' ')} was saved.")


# ── /start (private) ─────────────────────────────────────────────
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    # Reaction
    try:
        await message.react(emoji="😘")
    except Exception:
        pass

    # ── Start Animation ──────────────────────────────────────────
    emoji_splash = await message.reply_text(
        '<emoji id=5857183030543654930>🤩</emoji>  <emoji id=5854711294044677474>🤩</emoji>'
    )
    await asyncio.sleep(0.4)
    await emoji_splash.delete()

    loading = await message.reply_text(random.choice(GREET))
    await add_served_user(message.from_user.id)
    await asyncio.sleep(0.12)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ.<emoji id=5854949707679276482>🤩</emoji></b>')
    await asyncio.sleep(0.12)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ..<emoji id=5854767077079916825>🤩</emoji></b>')
    await asyncio.sleep(0.12)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ...<emoji id=5854767077079916825>🤩</emoji></b>')
    await asyncio.sleep(0.12)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ</b>')
    await asyncio.sleep(0.10)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ ✗</b>')
    await asyncio.sleep(0.10)
    await loading.edit_text('<b>ᴍᴀᴅᴀʀᴀ ✗ ᴍᴜsɪᴄ ♪</b>')
    await asyncio.sleep(0.10)
    await loading.edit_text('<b>sᴛᴀʀᴛᴇᴅ!<emoji id=5855072204441525267>🤩</emoji></b>')
    await asyncio.sleep(0.20)
    await loading.delete()
    # ── Animation End ────────────────────────────────────────────

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            await message.reply_photo(
                random.choice(MADARA_IMG),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
                message_effect_id=random.choice(EFFECT_IDS),
            )
        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                    ),
                )
        elif name.startswith("inf"):
            query = name.replace("info_", "", 1)
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(title, duration, views, published, channellink, channel, app.mention)
            key = InlineKeyboardMarkup([[
                InlineKeyboardButton(text=_["S_B_8"], url=link),
                InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
            ]])
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
                message_effect_id=random.choice(EFFECT_IDS),
            )
    else:
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()

        default_caption = _["start_2"].format(
            message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats
        )
        final_caption = await _get_caption("welcome_dm", default_caption, message.from_user, await client.get_me())

        await message.reply_photo(
            random.choice(MADARA_IMG),
            caption=final_caption,
            reply_markup=InlineKeyboardMarkup(out),
            message_effect_id=random.choice(EFFECT_IDS),
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                    f"<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )


# ── /start (group) ───────────────────────────────────────────────
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    # Reaction
    try:
        await message.react(emoji="😘")
    except Exception:
        pass

    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    default_caption = _["start_1"].format(app.mention, get_readable_time(uptime))
    final_caption = await _get_caption(
        "welcome_group", default_caption, message.from_user, await client.get_me(), message.chat
    )
    await message.reply_photo(
        random.choice(MADARA_IMG),
        caption=final_caption,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


# ── New member welcome ───────────────────────────────────────────
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                default_caption = _["start_3"].format(
                    message.from_user.mention, app.mention, message.chat.title, app.mention
                )
                final_caption = await _get_caption(
                    "welcome_group", default_caption, member, await client.get_me(), message.chat
                )
                await message.reply_photo(
                    random.choice(MADARA_IMG),
                    caption=final_caption,
                    reply_markup=InlineKeyboardMarkup(out),
                    message_effect_id=random.choice(EFFECT_IDS),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
