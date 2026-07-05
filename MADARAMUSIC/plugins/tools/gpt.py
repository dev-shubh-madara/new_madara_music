# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  MongoDB AI Chatbot — No External API Required   ║
# ╚══════════════════════════════════════════════════╝
import re
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from MADARAMUSIC import app
from MADARAMUSIC.core.mongo import mongodb
import config

# ── MongoDB collection ────────────────────────────────────────────
_kb = mongodb.chatbot_knowledge

# ── Default seed knowledge ────────────────────────────────────────
_SEED = [
    {
        "keywords": ["hello", "hi", "hey", "helo", "hii", "heyy", "howdy"],
        "answer": "👋 ʜᴇʟʟᴏ! ɪ'ᴍ *MADARA MUSIC* ʙᴏᴛ. ʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ? 🎵",
    },
    {
        "keywords": ["who", "are", "you", "bot", "name", "introduce", "yourself"],
        "answer": "🤖 ɪ ᴀᴍ *MADARA MUSIC* — ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ʙᴏᴛ!\n\n🎵 ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ, ᴍᴀɴᴀɢᴇ ǫᴜᴇᴜᴇs, ᴀɴᴅ ᴅᴏ ᴍᴜᴄʜ ᴍᴏʀᴇ!\n\n⚡ <tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
    },
    {
        "keywords": ["owner", "creator", "developer", "dev", "made", "who made"],
        "answer": f"👑 ᴍʏ ᴏᴡɴᴇʀ ɪs @{config.OWNER_USERNAME}\n\n🎵 <tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
    },
    {
        "keywords": ["play", "music", "song", "stream", "how to play"],
        "answer": "🎵 ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ, ᴜsᴇ:\n\n`/play [song name or YouTube link]`\n\n✅ ɪ sᴜᴘᴘᴏʀᴛ YouTube, Spotify, Apple Music & SoundCloud!\n\n⚡ <tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
    },
    {
        "keywords": ["skip", "next", "change", "track"],
        "answer": "⏭️ ᴛᴏ sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴏɴɢ:\n\n`/skip`\n\n✅ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ɪɴ ɢʀᴏᴜᴘs.",
    },
    {
        "keywords": ["stop", "end", "leave", "quit"],
        "answer": "⏹️ ᴛᴏ sᴛᴏᴘ sᴛʀᴇᴀᴍɪɴɢ:\n\n`/stop` or `/end`\n\n✅ ᴛʜɪs ᴡɪʟʟ ᴄʟᴇᴀʀ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ʟᴇᴀᴠᴇ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.",
    },
    {
        "keywords": ["pause", "resume"],
        "answer": "⏸️ Pause/Resume ᴄᴏᴍᴍᴀɴᴅs:\n\n`/pause` — ᴘᴀᴜsᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ\n`/resume` — ʀᴇsᴜᴍᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ",
    },
    {
        "keywords": ["queue", "playlist", "list", "songs", "queued"],
        "answer": "📋 ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ǫᴜᴇᴜᴇ:\n\n`/queue` — sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ ǫᴜᴇᴜᴇ\n\n✅ Yᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ sᴏɴɢs ᴀɴᴅ ᴛʜᴇʏ ᴡɪʟʟ ᴘʟᴀʏ ɪɴ ᴏʀᴅᴇʀ.",
    },
    {
        "keywords": ["ping", "speed", "fast", "slow", "response"],
        "answer": "⚡ ᴜsᴇ `/ping` ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ's ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ ᴀɴᴅ sᴇʀᴠᴇʀ sᴛᴀᴛs!",
    },
    {
        "keywords": ["help", "commands", "what can you do", "features"],
        "answer": "📖 ᴜsᴇ `/help` ᴛᴏ sᴇᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs!\n\n🎵 I have 100+ features including music, admin tools, games, crypto, and more!",
    },
    {
        "keywords": ["settings", "config", "configure"],
        "answer": "⚙️ ᴜsᴇ `/settings` ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ ᴛʜᴇ ʙᴏᴛ ꜰᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ.",
    },
    {
        "keywords": ["stats", "statistics", "info", "uptime"],
        "answer": "📊 ᴜsᴇ `/stats` ᴛᴏ sᴇᴇ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs.\n`/ping` ꜰᴏʀ sᴇʀᴠᴇʀ ɪɴꜰᴏ.",
    },
    {
        "keywords": ["loop", "repeat"],
        "answer": "🔁 Loop Mode:\n\n`/loop` — ᴛᴏɢɢʟᴇ ʟᴏᴏᴘ\n`/loop enable` — ᴇɴᴀʙʟᴇ ʟᴏᴏᴩ\n`/loop disable` — ᴅɪsᴀʙʟᴇ ʟᴏᴏᴩ",
    },
    {
        "keywords": ["volume", "vol", "loud", "quiet", "sound"],
        "answer": "🔊 Volume:\n\n`/vol [0-200]` — sᴇᴛ ᴠᴏʟᴜᴍᴇ\nᴇxᴀᴍᴘʟᴇ: `/vol 150`",
    },
    {
        "keywords": ["shuffle", "random", "mix"],
        "answer": "🔀 Shuffle:\n\n`/shuffle` — sʜᴜꜰꜰʟᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ǫᴜᴇᴜᴇ",
    },
    {
        "keywords": ["speed", "rate", "fast", "slow", "tempo"],
        "answer": "🚀 Playback Speed:\n\n`/speed [0.5-4.0]` — ᴄʜᴀɴɢᴇ sᴩᴇᴇᴅ\nᴇxᴀᴍᴘʟᴇ: `/speed 1.5`",
    },
    {
        "keywords": ["upi", "pay", "payment", "qr", "money"],
        "answer": "💳 UPI Payment:\n\n`/upi [UPI_ID]` — ɢᴇɴᴇʀᴀᴛᴇ ᴀ QR ᴄᴏᴅᴇ ꜰᴏʀ ᴀɴʏ UPI ɪᴅ",
    },
    {
        "keywords": ["crypto", "bitcoin", "ethereum", "ton", "usdt", "price", "coin"],
        "answer": "💰 Crypto Commands:\n\n`/ton` — TON ᴘʀɪᴄᴇ\n`/usdt` — Tether ᴩʀɪᴄᴇ\n`/tonbal [wallet]` — ᴄʜᴇᴄᴋ TON ᴡᴀʟʟᴇᴛ",
    },
    {
        "keywords": ["github", "git", "repo", "code"],
        "answer": f"🌐 GitHub Manager:\n\n`/github` — ᴍᴀɴᴀɢᴇ ɢɪᴛʜᴜʙ ʀᴇᴩᴏs\n\n🔗 Bot Repo: {config.UPSTREAM_REPO}",
    },
    {
        "keywords": ["afk", "away", "offline", "busy"],
        "answer": "🌙 AFK Mode:\n\n`/afk [reason]` — sᴇᴛ ʏᴏᴜʀsᴇʟꜰ ᴀs AFK\nBᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏ-ʀᴇᴩʟʏ ᴡʜᴇɴ ᴍᴇɴᴛɪᴏɴᴇᴅ.",
    },
    {
        "keywords": ["fight", "game", "chatfight", "word", "emoji"],
        "answer": "🎮 ChatFight Game:\n\n`/chatfight` — sᴛᴀʀᴛ ᴀ ᴡᴏʀᴅ/ᴇᴍᴏᴊɪ ɢᴀᴍᴇ\n`/gametop` — ᴠɪᴇᴡ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ",
    },
    {
        "keywords": ["broadcast", "announce", "message all"],
        "answer": "📢 Broadcast (Owner/Sudo only):\n\n`/broadcast [message]` — sᴇɴᴅ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴩs",
    },
    {
        "keywords": ["ban", "kick", "mute", "restrict"],
        "answer": "🔨 Admin Commands:\n\n`/ban` — ʙᴀɴ ᴀ ᴜsᴇʀ\n`/kick` — ᴋɪᴄᴋ ᴀ ᴜsᴇʀ\n`/mute` — ᴍᴜᴛᴇ ᴀ ᴜsᴇʀ\n\nReply to a user's message to use these.",
    },
    {
        "keywords": ["translate", "language", "lang", "hindi", "english"],
        "answer": "🌐 Translation:\n\n`/tr [language_code] [text]` — ᴛʀᴀɴsʟᴀᴛᴇ ᴛᴇxᴛ\nᴇxᴀᴍᴩʟᴇ: `/tr hi Hello world`",
    },
    {
        "keywords": ["weather", "temperature", "forecast", "climate"],
        "answer": "🌤️ Weather:\n\n`/weather [city]` — ɢᴇᴛ ᴡᴇᴀᴛʜᴇʀ ɪɴꜰᴏ\nᴇxᴀᴍᴩʟᴇ: `/weather Mumbai`",
    },
    {
        "keywords": ["sticker", "stickers", "pack"],
        "answer": "🎨 Stickers:\n\n`/kang` — ᴄʀᴇᴀᴛᴇ sᴛɪᴄᴋᴇʀ ꜰʀᴏᴍ ɪᴍᴀɢᴇ\n`/sticker` — ᴄᴏɴᴠᴇʀᴛ ɪᴍᴀɢᴇ ᴛᴏ sᴛɪᴄᴋᴇʀ",
    },
    {
        "keywords": ["what is love", "love", "relationship"],
        "answer": "❤️ Love is a beautiful feeling! 🌹\n\nBut for me, MUSIC is love! 🎵\n\nPlay your favorite song with `/play`",
    },
    {
        "keywords": ["joke", "funny", "laugh", "humor"],
        "answer": "😂 ᴜsᴇ `/joke` ꜰᴏʀ ʀᴀɴᴅᴏᴍ ᴊᴏᴋᴇs!\n\n🤣 ᴡʜʏ ᴅɪᴅ ᴛʜᴇ ᴍᴜsɪᴄɪᴀɴ ɢᴇᴛ ᴀʀʀᴇsᴛᴇᴅ?\nʙᴇᴄᴀᴜsᴇ ʜᴇ ɢᴏᴛ ᴄᴀᴜɢʜᴛ ɪɴ ᴀ ʙᴀss ᴄʟᴇꜰ! 🎵",
    },
    {
        "keywords": ["thanks", "thank you", "thx", "ty", "appreciate"],
        "answer": "😊 You're welcome! Always happy to help! 🎵\n\n⚡ <tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
    },
    {
        "keywords": ["support", "help me", "problem", "issue", "error"],
        "answer": f"🆘 ɴᴇᴇᴅ ʜᴇʟᴩ? ᴊᴏɪɴ ᴏᴜʀ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ:\n\n👉 {config.SUPPORT_CHAT}\n📢 {config.SUPPORT_CHANNEL}",
    },
    {
        "keywords": ["good morning", "morning", "gm"],
        "answer": "🌅 Good Morning! 🌞\n\nStart your day with some music! 🎵\nUse `/play` to get the beats going!",
    },
    {
        "keywords": ["good night", "night", "gn", "sleep"],
        "answer": "🌙 Good Night! 🌟\n\nSleep well and wake up to great music! 🎵",
    },
    {
        "keywords": ["how are you", "how r u", "how do you do", "sup", "wassup"],
        "answer": "😄 ɪ'ᴍ ᴅᴏɪɴɢ ɢʀᴇᴀᴛ, ᴛʜᴀɴᴋs ꜰᴏʀ ᴀsᴋɪɴɢ! 🎵\n\nAlways ready to stream music for you! Use `/play` to start!",
    },
]

_seeded = False


async def _ensure_seeded():
    """Seed default knowledge if the collection is empty."""
    global _seeded
    if _seeded:
        return
    count = await _kb.count_documents({})
    if count == 0:
        await _kb.insert_many(_SEED)
    _seeded = True


def _tokenize(text: str):
    """Simple tokenizer — lowercase words stripped of punctuation."""
    return set(re.sub(r"[^\w\s]", "", text.lower()).split())


async def _find_best_answer(query: str) -> str | None:
    """Find best matching answer using keyword overlap scoring."""
    q_tokens = _tokenize(query)
    if not q_tokens:
        return None

    best_score = 0
    best_answer = None

    async for doc in _kb.find({}):
        kw = set(doc.get("keywords", []))
        score = len(q_tokens & kw)
        if score > best_score:
            best_score = score
            best_answer = doc.get("answer")

    return best_answer if best_score > 0 else None


# ── /ai  /ask  /chatgpt  /gpt  /solve  ───────────────────────────
@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["/", "!", ".", "+"],
    ) & ~config.BANNED_USERS
)
async def chat_ai(bot, message: Message):
    await _ensure_seeded()

    if len(message.command) < 2:
        if message.reply_to_message and message.reply_to_message.text:
            query = message.reply_to_message.text
        else:
            return await message.reply_text(
                "❍ **ᴜsᴀɢᴇ:**\n\n`/ai [your question]`\n\n"
                "ᴇxᴀᴍᴩʟᴇ: `/ai how to play music`"
            )
    else:
        query = message.text.split(None, 1)[1]

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    answer = await _find_best_answer(query)

    if answer:
        await message.reply_text(
            f"<tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5213415326053582248\">H</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5213277251444952289\">U</tg-emoji><tg-emoji emoji-id=\"5212928963956983272\">S</tg-emoji><tg-emoji emoji-id=\"5211032856154885824\">I</tg-emoji><tg-emoji emoji-id=\"5210687171417097576\">C</tg-emoji>\n\n"
            f"🤖 **MADARA AI:**\n\n{answer}\n\n"
            f"<tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text(
            f"<tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5213415326053582248\">H</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5213277251444952289\">U</tg-emoji><tg-emoji emoji-id=\"5212928963956983272\">S</tg-emoji><tg-emoji emoji-id=\"5211032856154885824\">I</tg-emoji><tg-emoji emoji-id=\"5210687171417097576\">C</tg-emoji>\n\n"
            "🤔 ɪ ᴅɪᴅɴ'ᴛ ᴜɴᴅᴇʀsᴛᴀɴᴅ ᴛʜᴀᴛ.\n\n"
            "ᴛʀʏ ᴀsᴋɪɴɢ ᴀʙᴏᴜᴛ:\n"
            "• ʜᴏᴡ ᴛᴏ ᴩʟᴀʏ ᴍᴜsɪᴄ\n"
            "• ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n"
            "• ᴀᴅᴍɪɴ ᴛᴏᴏʟs\n"
            "• ɢᴀᴍᴇs & ᴛᴏᴏʟs\n\n"
            f"<tg-emoji emoji-id=\"5213095308040356426\">P</tg-emoji><tg-emoji emoji-id=\"5212943085809454431\">O</tg-emoji><tg-emoji emoji-id=\"5213148466850580086\">W</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5213337333742454261\">E</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji> <tg-emoji emoji-id=\"5213400521301313365\">B</tg-emoji><tg-emoji emoji-id=\"5210932667452768696\">Y</tg-emoji> <tg-emoji emoji-id=\"5210890482283988215\">M</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211094355791594395\">D</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji><tg-emoji emoji-id=\"5211009581727107238\">R</tg-emoji><tg-emoji emoji-id=\"5210820276748566172\">A</tg-emoji>",
            parse_mode=ParseMode.HTML,
        )


# ── /addqa — owner adds new Q&A ───────────────────────────────────
@app.on_message(
    filters.command("addqa", prefixes="/") & filters.user(config.OWNER_ID)
)
async def add_qa(bot, message: Message):
    await _ensure_seeded()
    usage = (
        "❍ **Usage:** `/addqa keywords... | answer`\n\n"
        "ᴇxᴀᴍᴩʟᴇ:\n`/addqa music play stream | To play music use /play command`"
    )
    if len(message.command) < 2:
        return await message.reply_text(usage)

    text = message.text.split(None, 1)[1]
    if "|" not in text:
        return await message.reply_text(usage)

    parts = text.split("|", 1)
    keywords = [k.strip().lower() for k in parts[0].split() if k.strip()]
    answer = parts[1].strip()

    if not keywords or not answer:
        return await message.reply_text(usage)

    await _kb.insert_one({"keywords": keywords, "answer": answer})
    await message.reply_text(
        f"✅ **Q&A Added!**\n\n"
        f"🔑 **Keywords:** `{', '.join(keywords)}`\n"
        f"💬 **Answer:** {answer[:100]}{'...' if len(answer) > 100 else ''}"
    )


# ── /listqa — show all Q&A entries ───────────────────────────────
@app.on_message(
    filters.command("listqa", prefixes="/") & filters.user(config.OWNER_ID)
)
async def list_qa(bot, message: Message):
    await _ensure_seeded()
    count = await _kb.count_documents({})
    lines = [f"📚 **Chatbot Knowledge Base** — {count} entries\n"]
    idx = 1
    async for doc in _kb.find({}, {"keywords": 1, "answer": 1}).limit(30):
        kws = ", ".join(doc.get("keywords", [])[:5])
        preview = str(doc.get("answer", ""))[:60].replace("\n", " ")
        lines.append(f"{idx}. `{kws}` → {preview}…")
        idx += 1
    if count > 30:
        lines.append(f"\n_(showing 30 of {count})_")
    lines.append("\nᴜsᴇ `/addqa keywords | answer` ᴛᴏ ᴀᴅᴅ.\nᴜsᴇ `/deleteqa keyword` ᴛᴏ ᴅᴇʟᴇᴛᴇ.")
    await message.reply_text("\n".join(lines))


# ── /deleteqa — remove Q&A entry ─────────────────────────────────
@app.on_message(
    filters.command("deleteqa", prefixes="/") & filters.user(config.OWNER_ID)
)
async def delete_qa(bot, message: Message):
    await _ensure_seeded()
    if len(message.command) < 2:
        return await message.reply_text("❍ **Usage:** `/deleteqa [keyword]`")

    keyword = message.command[1].lower()
    result = await _kb.delete_one({"keywords": keyword})
    if result.deleted_count:
        await message.reply_text(f"✅ Deleted entry with keyword: `{keyword}`")
    else:
        await message.reply_text(f"❌ No entry found with keyword: `{keyword}`")
