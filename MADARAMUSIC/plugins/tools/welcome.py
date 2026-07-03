# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  Welcome Card — New Premium Template             ║
# ╚══════════════════════════════════════════════════╝
import os
import random
import asyncio
from logging import getLogger

from pyrogram import Client, filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode, ChatMemberStatus
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops, ImageFilter

from MADARAMUSIC import app
from MADARAMUSIC.utils.database import add_served_chat, get_assistant, is_active_chat
from MADARAMUSIC.misc import SUDOERS
from MADARAMUSIC.utils.emojis import E_HEART, E_SPARK, E_STAR, E_MUSIC, E_CROWN

LOGGER = getLogger(__name__)

# ── Asset paths ─────────────────────────────────────────────
_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets")

def _asset(name: str) -> str:
    return os.path.join(_ASSETS, name)

# ── Welcome background — new premium image ──────────────────
WELCOME_BG   = _asset("welcome_new.png")  # 1448×1086 source
FALLBACK_BG  = _asset("wel2.png")

# ── Girl pics for random sends ───────────────────────────────
GIRL_PICS = [_asset(f"girl{i}.png") for i in range(1, 5)]


class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        self.data.setdefault(chat_id, {"state": "on"})

    async def rm_wlcm(self, chat_id):
        self.data.pop(chat_id, None)


wlcm = WelDatabase()


class temp:
    ME      = None
    CURRENT = 2
    CANCEL  = False
    MELCOW  = {}
    U_NAME  = None
    B_NAME  = None


def _circle_crop(img: Image.Image, size: tuple) -> Image.Image:
    """Return circular-cropped, RGBA image."""
    img = img.resize(size, Image.LANCZOS).convert("RGBA")
    img = ImageEnhance.Brightness(img).enhance(1.1)
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, img.split()[-1])
    img.putalpha(mask)
    return img


def _draw_ring(draw: ImageDraw.Draw, cx: int, cy: int, r: int, width: int = 8):
    """Draw a glowing ring around the profile picture."""
    for col, w in [((100, 200, 255, 220), width + 4), ((255, 255, 255, 255), width)]:
        draw.ellipse(
            [cx - r - w // 2, cy - r - w // 2, cx + r + w // 2, cy + r + w // 2],
            outline=col, width=3,
        )


def welcomepic(pic: str, user: str, chatname: str, user_id: int, uname: str | None) -> str:
    os.makedirs("downloads", exist_ok=True)

    # ── Load & crop background ───────────────────────────────
    bg_path = WELCOME_BG if os.path.exists(WELCOME_BG) else (FALLBACK_BG if os.path.exists(FALLBACK_BG) else None)
    if bg_path:
        src = Image.open(bg_path).convert("RGBA")
        # Resize to fill 1280 wide, then centre-crop to 1280×720
        scale  = 1280 / src.width
        new_h  = int(src.height * scale)
        src    = src.resize((1280, new_h), Image.LANCZOS)
        top    = max(0, (new_h - 720) // 2)
        bg     = src.crop((0, top, 1280, top + 720))
    else:
        bg = Image.new("RGBA", (1280, 720), (10, 10, 30, 255))

    # Slightly darken to make text pop
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 90))
    bg      = Image.alpha_composite(bg, overlay)

    # ── Profile picture circle ───────────────────────────────
    # Center of the circular frame in the welcome template:
    #   source circle is at ~50% width, ~38% height of 1448×1086.
    #   After scale + crop:
    #     cx = 640  (50% of 1280)
    #     cy raw = 1086*0.38 * (1280/1448) = ~366; after top-crop ~120 px → ~246
    CIRCLE_SIZE = (240, 240)
    CX, CY      = 640, 246
    pfp_img     = _circle_crop(Image.open(pic).convert("RGBA"), CIRCLE_SIZE)
    px          = CX - CIRCLE_SIZE[0] // 2
    py          = CY - CIRCLE_SIZE[1] // 2
    bg.paste(pfp_img, (px, py), pfp_img)

    # Ring glow around profile pic
    draw = ImageDraw.Draw(bg, "RGBA")
    _draw_ring(draw, CX, CY, CIRCLE_SIZE[0] // 2 + 6)

    # ── Fonts ────────────────────────────────────────────────
    try:
        f_big  = ImageFont.truetype(_asset("font.ttf"), 54)
        f_med  = ImageFont.truetype(_asset("font.ttf"), 34)
        f_sm   = ImageFont.truetype(_asset("font.ttf"), 26)
    except Exception:
        f_big = f_med = f_sm = ImageFont.load_default()

    # ── Text block — right of centre ─────────────────────────
    TX = 700
    TY = 420
    draw.text((TX, TY),       "ᴡᴇʟᴄᴏᴍᴇ",              fill=(255, 80, 180), font=f_big, anchor="lm")
    draw.text((TX, TY + 68),  f"ɴᴀᴍᴇ : {user[:22]}",   fill=(255, 255, 255), font=f_med, anchor="lm")
    draw.text((TX, TY + 115), f"ɪᴅ   : {user_id}",     fill=(180, 200, 255), font=f_sm,  anchor="lm")
    draw.text((TX, TY + 150), f"ᴜ    : @{uname or 'None'}", fill=(180, 255, 200), font=f_sm, anchor="lm")
    draw.text((TX, TY + 185), f"ɢʀᴏᴜᴘ : {chatname[:22]}", fill=(255, 180, 200), font=f_sm, anchor="lm")

    out = f"downloads/welcome_{user_id}.png"
    bg.convert("RGB").save(out, quality=95)
    return out


# ─────────────────────────────────────────────────────────────
@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = (
        "<blockquote><b>⚡ ᴡᴇʟᴄᴏᴍᴇ ᴄᴏᴍᴍᴀɴᴅ</b></blockquote>\n\n"
        "✅ <code>/welcome on</code> — Enable welcome card\n"
        "❌ <code>/welcome off</code> — Disable welcome card"
    )
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    member  = await app.get_chat_member(chat_id, message.from_user.id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text(
            "❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴡᴇʟᴄᴏᴍᴇ sᴇᴛᴛɪɴɢs!</b>",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close",
)
            ]]),
        )

    A     = await wlcm.find_one(chat_id)
    state = message.text.split(None, 1)[1].strip().lower()

    if state == "off":
        if A:
            await message.reply_text("⚠️ <b>ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ!</b>")
        else:
            await wlcm.add_wlcm(chat_id)
            await message.reply_text(
                f"❌ <b>ᴡᴇʟᴄᴏᴍᴇ ᴅɪsᴀʙʟᴇᴅ ɪɴ</b> {message.chat.title}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ ᴇɴᴀʙʟᴇ ᴀɢᴀɪɴ", callback_data="welcome_on",
)
                ]]),
            )
    elif state == "on":
        if not A:
            await message.reply_text("⚠️ <b>ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ!</b>")
        else:
            await wlcm.rm_wlcm(chat_id)
            await message.reply_text(
                f"✅ <b>ᴡᴇʟᴄᴏᴍᴇ ᴇɴᴀʙʟᴇᴅ ɪɴ</b> {message.chat.title}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("❌ ᴅɪsᴀʙʟᴇ", callback_data="welcome_off",
)
                ]]),
            )
    else:
        await message.reply_text(usage)


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id

    A = await wlcm.find_one(chat_id)
    if A:
        return

    if not (member.new_chat_member and not member.old_chat_member):
        return
    if member.new_chat_member.status == "kicked":
        return

    user  = member.new_chat_member.user
    count = await app.get_chat_members_count(chat_id)

    try:
        pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
    except Exception:
        pic = _asset("upic.png")

    old = temp.MELCOW.get(f"welcome-{chat_id}")
    if old:
        try:
            await old.delete()
        except Exception:
            pass

    try:
        welcomeimg = welcomepic(
            pic,
            user.first_name or "User",
            member.chat.title or "Group",
            user.id,
            user.username,
        )

        msg = await app.send_photo(
            chat_id,
            photo=welcomeimg,
            caption=(
                f"<emoji id='{E_CROWN}'>👑</emoji> <blockquote><b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ!</b></blockquote>\n\n"
                f"<emoji id='{E_MUSIC}'>🎵</emoji> <b>ɴᴀᴍᴇ :</b> {user.mention}\n"
                f"<emoji id='{E_STAR}'>⭐</emoji> <b>ɪᴅ   :</b> <code>{user.id}</code>\n"
                f"<emoji id='{E_HEART}'>❤️</emoji> <b>ᴜsᴇʀ :</b> @{user.username or 'None'}\n"
                f"<emoji id='{E_SPARK}'>✨</emoji> <b>ᴍᴇᴍʙᴇʀs :</b> {count}\n\n"
                f"<i>⭐ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ғᴀᴍɪʟʏ!</i>"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ",
                        url=f"tg://openmessage?user_id={user.id}",
                    ),
                    InlineKeyboardButton(
                        "➕ ᴀᴅᴅ ᴛᴏ ɢʀᴏᴜᴘ",
                        url=f"https://t.me/{app.username}?startgroup=true",
                    ),
                ],
            ]),
        )
        temp.MELCOW[f"welcome-{chat_id}"] = msg

        if pic != _asset("upic.png"):
            try:
                os.remove(pic)
            except Exception:
                pass
        try:
            os.remove(welcomeimg)
        except Exception:
            pass

        await asyncio.sleep(300)
        try:
            await msg.delete()
        except Exception:
            pass

    except Exception as e:
        LOGGER.error(f"[welcome] error: {e}")
