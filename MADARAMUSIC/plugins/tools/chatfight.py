# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  Chat Fight — Word / Emoji / Flag Games          ║
# ╚══════════════════════════════════════════════════╝
import asyncio
import os
import random
import time
import uuid

from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MADARAMUSIC import app
from MADARAMUSIC.core.mongo import mongodb
from MADARAMUSIC.utils.emojis import (
    E_FIRE, E_CROWN, E_STAR, E_THUNDER, E_SPARK, E_CLOSE,
    E_HEART, E_DIAMOND, E_GLOBE, E_GEAR,
)

# ── MongoDB ──────────────────────────────────────────────
game_db  = mongodb["chatfight_leaderboard"]

# ── Asset paths ─────────────────────────────────────────
_ASSETS   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets")
TEMPLATE  = os.path.join(_ASSETS, "chatfight_bg.png")
FONT_PATH = os.path.join(_ASSETS, "font.ttf")

# ── Global state ─────────────────────────────────────────
active_games:      dict = {}   # chat_id → game dict
user_cooldowns:    dict = {}
last_message_time: dict = {}
INACTIVITY_LIMIT = 300   # seconds before auto-game
PENALTY_TIME     = 60

# ── Small-caps converter ─────────────────────────────────
_SC = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
)
def sc(text: str) -> str:
    return str(text).translate(_SC)

# ── Word bank ─────────────────────────────────────────────
WORDS = [
    "python","music","telegram","stream","audio","video","player",
    "loop","queue","shuffle","speed","search","download","upload",
    "premium","diamond","crown","thunder","spark","heart","fire",
    "globe","gear","star","song","artist","album","playlist","channel",
    "group","admin","sudo","bot","broadcast","language","setting",
    "support","command","feature","version","update","restart","ping",
    "stats","uptime","server","database","mongo","token","session",
    "github","branch","commit","issue","repository","keyboard","inline",
    "button","emoji","sticker","photo","voice","call","message","reply",
]

# ── Emoji guess bank ─────────────────────────────────────
EMOJI_GAMES = [
    ("🍕", "pizza"), ("🍔", "burger"), ("🍣", "sushi"), ("🍜", "noodles"),
    ("🍦", "icecream"), ("🍩", "donut"), ("🎂", "cake"), ("🍟", "fries"),
    ("🚀", "rocket"), ("🎸", "guitar"), ("🎹", "piano"), ("🎧", "headphone"),
    ("🏆", "trophy"), ("💻", "laptop"), ("📱", "mobile"), ("⚽", "football"),
    ("🏏", "cricket"), ("🎯", "target"), ("🔑", "key"), ("💎", "diamond"),
]

# ── Flag/country bank ────────────────────────────────────
FLAG_GAMES = [
    ("🇮🇳", "india"), ("🇺🇸", "usa"), ("🇯🇵", "japan"), ("🇧🇷", "brazil"),
    ("🇨🇦", "canada"), ("🇬🇧", "uk"), ("🇫🇷", "france"), ("🇩🇪", "germany"),
    ("🇮🇹", "italy"), ("🇷🇺", "russia"), ("🇨🇳", "china"), ("🇦🇺", "australia"),
    ("🇪🇸", "spain"), ("🇲🇽", "mexico"), ("🇰🇷", "korea"), ("🇸🇦", "saudi"),
    ("🇵🇰", "pakistan"), ("🇧🇩", "bangladesh"), ("🇳🇬", "nigeria"), ("🇿🇦", "south africa"),
]


# ── Build game card image ─────────────────────────────────
def build_game_card(line1: str, line2: str, hint: str) -> str:
    os.makedirs("cache", exist_ok=True)
    out = f"cache/chatfight_{uuid.uuid4().hex}.png"
    try:
        bg = Image.open(TEMPLATE).convert("RGBA").resize((1280, 720))
        overlay = Image.new("RGBA", bg.size, (0, 0, 0, 140))
        bg = Image.alpha_composite(bg, overlay)
        draw = ImageDraw.Draw(bg)
        try:
            f_big = ImageFont.truetype(FONT_PATH, 64)
            f_med = ImageFont.truetype(FONT_PATH, 40)
            f_sm  = ImageFont.truetype(FONT_PATH, 30)
        except Exception:
            f_big = f_med = f_sm = ImageFont.load_default()

        # title
        draw.text((640, 120), "⚔️  CHAT FIGHT  ⚔️", fill=(255, 215, 0), font=f_big, anchor="mm")
        draw.text((640, 320), line1, fill=(255, 255, 255), font=f_big, anchor="mm")
        draw.text((640, 420), line2, fill=(200, 230, 255), font=f_med, anchor="mm")
        draw.text((640, 560), hint, fill=(180, 180, 180), font=f_sm, anchor="mm")

        bg.convert("RGB").save(out)
    except Exception:
        return TEMPLATE
    return out


# ── Scramble helper ───────────────────────────────────────
def scramble(word: str) -> str:
    chars = list(word)
    while "".join(chars) == word:
        random.shuffle(chars)
    return "".join(chars)


# ── Start games ───────────────────────────────────────────
async def start_word_game(chat_id: int):
    if chat_id in active_games:
        return
    word   = random.choice(WORDS)
    jumbled = scramble(word)
    hint   = f"⚡ ᴡᴏʀᴅ ʜᴀs {len(word)} ʟᴇᴛᴛᴇʀs"
    img    = build_game_card("🔤 ᴡᴏʀᴅ ɢᴀᴍᴇ", jumbled.upper(), hint)
    try:
        msg = await app.send_photo(
            chat_id, photo=img,
            caption=(
                f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>{sc('Word Game Started!')}</b>\n\n"
                f"<emoji id='{E_SPARK}'>✨</emoji> <b>{sc('Unscramble this word:')}</b>\n"
                f"<blockquote><b>🔤 {jumbled.upper()}</b></blockquote>\n"
                f"<i>{hint}</i>\n\n"
                f"<emoji id='{E_STAR}'>⭐</emoji> <i>{sc('First correct answer gets +10 points!')}</i>"
            ),
        )
        active_games[chat_id] = {
            "type": "word", "answer": word, "message_id": msg.id,
            "start_time": time.time(), "winners": [],
        }
        try:
            os.remove(img)
        except Exception:
            pass
    except Exception:
        pass


async def start_emoji_game(chat_id: int):
    if chat_id in active_games:
        return
    emoji, answer = random.choice(EMOJI_GAMES)
    img = build_game_card("😀 ᴇᴍᴏᴊɪ ɢᴜᴇss", emoji, "ᴡʜᴀᴛ ᴅᴏᴇs ᴛʜɪs ʀᴇᴘʀᴇsᴇɴᴛ?")
    try:
        msg = await app.send_photo(
            chat_id, photo=img,
            caption=(
                f"<emoji id='{E_FIRE}'>🔥</emoji> <b>{sc('Emoji Guess Game!')}</b>\n\n"
                f"<emoji id='{E_SPARK}'>✨</emoji> <b>{sc('What does this emoji represent?')}</b>\n"
                f"<blockquote><b>{emoji}</b></blockquote>\n\n"
                f"<emoji id='{E_STAR}'>⭐</emoji> <i>{sc('First correct answer gets +10 points!')}</i>"
            ),
        )
        active_games[chat_id] = {
            "type": "emoji", "answer": answer, "message_id": msg.id,
            "start_time": time.time(), "winners": [],
        }
        try:
            os.remove(img)
        except Exception:
            pass
    except Exception:
        pass


async def start_flag_game(chat_id: int):
    if chat_id in active_games:
        return
    flag, answer = random.choice(FLAG_GAMES)
    img = build_game_card("🌍 ғʟᴀɢ ɢᴜᴇss", flag, "ᴡʜɪᴄʜ ᴄᴏᴜɴᴛʀʏ ɪs ᴛʜɪs?")
    try:
        msg = await app.send_photo(
            chat_id, photo=img,
            caption=(
                f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>{sc('Flag Guess Game!')}</b>\n\n"
                f"<emoji id='{E_SPARK}'>✨</emoji> <b>{sc('Which country does this flag belong to?')}</b>\n"
                f"<blockquote><b>{flag}</b></blockquote>\n\n"
                f"<emoji id='{E_STAR}'>⭐</emoji> <i>{sc('First correct answer gets +10 points!')}</i>"
            ),
        )
        active_games[chat_id] = {
            "type": "flag", "answer": answer, "message_id": msg.id,
            "start_time": time.time(), "winners": [],
        }
        try:
            os.remove(img)
        except Exception:
            pass
    except Exception:
        pass


# ── /chatfight command ────────────────────────────────────
@app.on_message(filters.command(["chatfight", "cf"]) & filters.group)
async def chatfight_cmd(client, message: Message):
    if message.chat.id in active_games:
        return await message.reply_text(
            f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>{sc('A game is already running in this group!')}</b>"
        )
    game_type = random.choice(["word", "emoji", "flag"])
    if game_type == "word":
        await start_word_game(message.chat.id)
    elif game_type == "emoji":
        await start_emoji_game(message.chat.id)
    else:
        await start_flag_game(message.chat.id)


# ── Answer listener ───────────────────────────────────────
@app.on_message(filters.group & filters.text & ~filters.command([]))
async def game_answer_listener(client, message: Message):
    chat_id = message.chat.id
    last_message_time[chat_id] = time.time()

    game = active_games.get(chat_id)
    if not game:
        return

    if not message.from_user:
        return   # skip anonymous / channel posts
    user_id   = message.from_user.id
    user_name = message.from_user.first_name or "User"
    text      = message.text.strip().lower()
    answer    = game["answer"].lower()

    # cooldown check
    now = time.time()
    last_cd = user_cooldowns.get((chat_id, user_id), 0)
    if now - last_cd < 3:
        return

    # accept if close enough
    if text == answer or (len(answer) > 4 and answer in text):
        user_cooldowns[(chat_id, user_id)] = now
        del active_games[chat_id]

        # update leaderboard
        doc = await game_db.find_one({"user_id": user_id})
        if doc:
            await game_db.update_one(
                {"user_id": user_id},
                {"$set": {"name": user_name, "points": doc["points"] + 10}},
            )
        else:
            await game_db.insert_one({"user_id": user_id, "name": user_name, "points": 10})

        try:
            await message.reply_text(
                f"<emoji id='{E_CROWN}'>👑</emoji> <b>{message.from_user.mention} {sc('won!')}</b>\n\n"
                f"<emoji id='{E_STAR}'>⭐</emoji> <b>{sc('Correct Answer:')} <code>{game['answer'].upper()}</code></b>\n"
                f"<emoji id='{E_DIAMOND}'>💎</emoji> <i>{sc('+10 points added to global ranking!')}</i>",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        f"🏆 {sc('Leaderboard')}",
                        callback_data="chatfight_leaderboard",
                    ),
                ]]),
            )
        except Exception:
            pass


# ── Leaderboard ───────────────────────────────────────────
@app.on_message(filters.command(["gametop", "wordleaderboard", "chatfighttop"]) & filters.group)
async def game_leaderboard_cmd(client, message: Message):
    await _send_leaderboard(message)


@app.on_callback_query(filters.regex("chatfight_leaderboard"))
async def game_leaderboard_cb(client, cq):
    await cq.answer()
    await _send_leaderboard(cq.message)


async def _send_leaderboard(msg):
    top = game_db.find().sort("points", -1).limit(10)
    text = (
        f"<emoji id='{E_CROWN}'>👑</emoji> <b>{sc('Chat Fight — Global Leaderboard')}</b>\n"
        f"<emoji id='{E_FIRE}'>🔥</emoji> <b>{sc('Top 10 Players')}</b>\n\n"
    )
    count = 1
    has_users = False
    medals = ["🥇", "🥈", "🥉"]
    async for user in top:
        has_users = True
        medal = medals[count - 1] if count <= 3 else f"<b>{count}.</b>"
        text += f"{medal} {sc(user.get('name', 'Unknown'))} — <code>{user['points']}</code> pts\n"
        count += 1
    if not has_users:
        text += f"<i>{sc('No one has scored yet! Start a game with /chatfight')}</i>"

    try:
        await msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    f"⚔️ {sc('Play Again')}",
                    callback_data="chatfight_start",
                ),
            ]]),
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex("chatfight_start"))
async def chatfight_start_cb(client, cq):
    await cq.answer()
    await chatfight_cmd(client, cq.message)


# ── Inactivity loop ────────────────────────────────────────
async def inactivity_checker():
    while True:
        await asyncio.sleep(60)
        now = time.time()
        # clean stale games (>10 min)
        for chat_id, game in list(active_games.items()):
            if now - game["start_time"] > 600:
                try:
                    await app.delete_messages(chat_id, game["message_id"])
                except Exception:
                    pass
                del active_games[chat_id]
        # auto-start on inactivity
        for chat_id, last_t in list(last_message_time.items()):
            if now - last_t > INACTIVITY_LIMIT and chat_id not in active_games:
                try:
                    pick = random.choice(["word", "emoji", "flag"])
                    if pick == "word":
                        await start_word_game(chat_id)
                    elif pick == "emoji":
                        await start_emoji_game(chat_id)
                    else:
                        await start_flag_game(chat_id)
                except Exception:
                    pass

asyncio.create_task(inactivity_checker())
