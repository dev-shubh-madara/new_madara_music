import asyncio
import random
import html
import time
from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from py_yt import VideosSearch

import config
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import _boot_
from SHUKLAMUSIC.plugins.sudo.sudoers import sudoers_list
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)

# --- DATABASE FIX (Ping Jaisa) ---
try:
    from SHUKLAMUSIC.core.mongo import mongodb as db
except ImportError:
    try:
        from SHUKLAMUSIC.utils.database import mongodb as db
    except ImportError:
        from SHUKLAMUSIC.core.mongo import mongodb
        db = mongodb

from SHUKLAMUSIC.utils.decorators.language import LanguageStart
from SHUKLAMUSIC.utils.formatters import get_readable_time
from SHUKLAMUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# ================================
#        DATABASE SETUP
# ================================
welcome_db = db.welcome_config 

YUMI_PICS = [
"https://files.catbox.moe/5go4t6.jpg",
"https://files.catbox.moe/vbdda6.jpg",
"https://files.catbox.moe/l2id2z.jpg",  

]

GREET = [
    "💞", "🥂", "🔍", "🧪", "🥂", "⚡️", "🔥",
]

async def delete_sticker_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

# ================================
#      SET WELCOME COMMANDS
# ================================
# Yahan maine filter change karke aapki ID laga di hai (Ping jaisa)
@app.on_message(filters.command(["setwelcome_dm", "setwelcome_grp"]) & filters.user(7553434931))
async def set_welcome_msg(client, message):
    cmd = message.command[0].lower()
    msg_type = "welcome_dm" if "dm" in cmd else "welcome_group"

    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            f"❌ <b>Usage:</b>\n<code>/{cmd} [Your HTML Message]</code>\n\n"
            "<b>Variables:</b>\n"
            "<code>{name}</code> - First Name\n"
            "<code>{mention}</code> - User Link\n"
            "<code>{username}</code> - @Username\n"
            "<code>{bot_name}</code> - Bot Name\n"
            "<code>{chat_name}</code> - Chat Name (Group only)"
        )
        return

    # Extract Text (Preserving HTML for Premium Emojis)
    try:
        if message.reply_to_message:
            new_msg = message.reply_to_message.text.html or message.reply_to_message.caption.html
        else:
            new_msg = message.text.html.split(None, 1)[1]
    except (IndexError, AttributeError):
         return await message.reply_text("❌ Text extract nahi kar paya. Dobara try karein.")

    # Save to Database
    await welcome_db.update_one(
        {"_id": msg_type},
        {"$set": {"message": new_msg}},
        upsert=True
    )
    
    await message.reply_text(f"✅ <b>{msg_type.replace('_', ' ').upper()} message has been set!</b>")


@app.on_message(filters.command(["resetwelcome"]) & filters.user(7553434931))
async def reset_welcome_msg(client, message):
    cmd_args = message.command
    msg_type = "welcome_dm"
    if len(cmd_args) > 1 and cmd_args[1].lower() in ("grp", "group"):
        msg_type = "welcome_group"
    result = await welcome_db.delete_one({"_id": msg_type})
    if result.deleted_count:
        await message.reply_text(
            f"✅ <b>{msg_type.replace('_', ' ').upper()} reset!</b>\n"
            "<i>Bot will now use the default start message from en.yml (with new Crypto & UPI features).</i>"
        )
    else:
        await message.reply_text(
            f"ℹ️ <b>No custom {msg_type.replace('_', ' ')} was saved.</b>\n"
            "<i>Already using the default message.</i>"
        )

# Helper to get welcome text
async def get_welcome_caption(msg_type, default_text, user, bot, chat=None):
    data = await welcome_db.find_one({"_id": msg_type})
    
    if data and "message" in data:
        text = data["message"]
        # Replace Placeholders
        text = text.replace("{name}", user.first_name)
        text = text.replace("{mention}", user.mention)
        text = text.replace("{username}", f"@{user.username}" if user.username else "No Username")
        text = text.replace("{bot_name}", bot.first_name)
        if chat:
            text = text.replace("{chat_name}", chat.title)
        return text
    
    return default_text

# ================================
#        START COMMAND (DM)
# ================================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    
    # --- REACTION START ---
    try:
        await message.react(emoji="😘")
    except Exception:
        pass
    # --- REACTION END ---

    # --- ANIMATION START ---
    # Step 1 — Send 2 premium emojis from radhamusicbot1_by_TgEmojis_bot
    emoji_splash = await message.reply_text(
        '<emoji id=5857183030543654930>🤩</emoji>  <emoji id=5854711294044677474>🤩</emoji>'
    )
    await asyncio.sleep(0.5)
    await emoji_splash.delete()

    # Step 2 — Writing animation
    loading_1 = await message.reply_text(random.choice(GREET))
    await add_served_user(message.from_user.id)

    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ.<emoji id=5854949707679276482>🤩</emoji></b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ..<emoji id=5854767077079916825>🤩</emoji></b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ...<emoji id=5854767077079916825>🤩</emoji></b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ʀᴀᴅʜᴀ</b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ʀᴀᴅʜᴀ ꭙ</b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>ʀᴀᴅʜᴀ ꭙ ϻᴜsɪᴄ ♪</b>")
    await asyncio.sleep(0.1)
    await loading_1.edit_text("<b>sᴛᴧʀᴛed!<emoji id=5855072204441525267>🤩</emoji></b>")
    await asyncio.sleep(0.1)
    await loading_1.delete()
    # --- ANIMATION END ---

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_photo(
                random.choice(YUMI_PICS),
                has_spoiler=True,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
        elif name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = str(name).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
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
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_video(
                chat_id=message.chat.id,
                video=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
    else:
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        
        # --- GET CUSTOM OR DEFAULT CAPTION ---
        default_caption = _["start_2"].format(
            message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats
        )
        
        # Checking DB for Custom DM Message
        final_caption = await get_welcome_caption(
            "welcome_dm", 
            default_caption, 
            message.from_user, 
            await client.get_me()
        )

        await message.reply_photo(
            random.choice(YUMI_PICS),
            has_spoiler=True,
            caption=final_caption,
            reply_markup=InlineKeyboardMarkup(out),
        )
        
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

# ================================
#        START COMMAND (GROUP)
# ================================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    # --- REACTION START ---
    try:
        await message.react(emoji="😘")
    except Exception:
        pass
    # --- REACTION END ---
    
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    
    # --- GET CUSTOM OR DEFAULT CAPTION ---
    default_caption = _["start_1"].format(app.mention, get_readable_time(uptime))
    
    final_caption = await get_welcome_caption(
        "welcome_group", 
        default_caption, 
        message.from_user, 
        await client.get_me(),
        message.chat
    )

    await message.reply_photo(
        random.choice(YUMI_PICS),
        caption=final_caption,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

# ================================
#        NEW MEMBER WELCOME
# ================================
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
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
                
                # --- GET CUSTOM OR DEFAULT CAPTION ---
                default_caption = _["start_3"].format(
                    message.from_user.mention,
                    app.mention,
                    message.chat.title,
                    app.mention,
                )
                
                final_caption = await get_welcome_caption(
                    "welcome_group", 
                    default_caption, 
                    member, # Passing the new member object
                    await client.get_me(),
                    message.chat
                )

                await message.reply_photo(
                    random.choice(YUMI_PICS),
                    has_spoiler=True,
                    caption=final_caption,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
