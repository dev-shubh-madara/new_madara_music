# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  String Session Generator — Pyro v1/v2 & Tele   ║
# ╚══════════════════════════════════════════════════╝
import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)

from MADARAMUSIC import app
from MADARAMUSIC.utils.emojis import (
    E_KEY, E_SPARK, E_CLOSE, E_STAR, E_THUNDER, E_DIAMOND,
    E_HEART, E_CROWN, E_GEAR, E_FIRE,
)
import config

# ── State store (user_id → session data) ──────────────────
_sessions: dict = {}

_API_ID   = config.API_ID
_API_HASH = config.API_HASH

def _markup_type():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 Pyrogram V2",
                callback_data="gs_pyro2",
            ),
        ],
        [
            InlineKeyboardButton(
                "⭐ Pyrogram V1",
                callback_data="gs_pyro1",
            ),
        ],
        [
            InlineKeyboardButton(
                "⚡ Telethon",
                callback_data="gs_tele",
            ),
        ],
        [
            InlineKeyboardButton(
                "✖️ Cancel",
                callback_data="gs_cancel",
            ),
        ],
    ])


def _markup_cancel():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "✖️ Cancel",
            callback_data="gs_cancel",
        ),
    ]])


# ── /genstring ────────────────────────────────────────────
@app.on_message(filters.command(["genstring", "gensession", "string"]) & filters.private)
async def genstring_start(client, message: Message):
    uid = message.from_user.id
    _sessions.pop(uid, None)
    await message.reply_text(
        f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ᴘʀᴇᴍɪᴜᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ</b>\n\n"
        f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴄʜᴏᴏsᴇ ᴛʜᴇ sᴇssɪᴏɴ ᴛʏᴘᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ :</b>\n\n"
        f"• <b>Pyrogram V2</b> — ᴘʏʀᴏғᴏʀᴋ / ᴘʏʀᴏɢʀᴀᴍ ᴠ2\n"
        f"• <b>Pyrogram V1</b> — ʟᴇɢᴀᴄʏ ᴘʏʀᴏɢʀᴀᴍ ᴠ1\n"
        f"• <b>Telethon</b> — ᴛᴇʟᴇᴛʜᴏɴ ʟɪʙʀᴀʀʏ\n\n"
        f"<emoji id='{E_SPARK}'>✨</emoji> <i>ᴀʟʟ sᴇssɪᴏɴs ᴀʀᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ sᴇᴄᴜʀᴇʟʏ ᴀɴᴅ ɴᴇᴠᴇʀ sᴛᴏʀᴇᴅ.</i>",
        reply_markup=_markup_type(),
    )


# ── Group redirect ────────────────────────────────────────
@app.on_message(filters.command(["genstring", "gensession", "string"]) & filters.group)
async def genstring_group(client, message: Message):
    await message.reply_text(
        f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ᴍʏ ᴅᴍ ғᴏʀ sᴇᴄᴜʀɪᴛʏ!</b>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔑 ɢᴇɴᴇʀᴀᴛᴇ sᴛʀɪɴɢ",
                url=f"https://t.me/{app.username}?start=genstring",
            ),
        ]]),
    )


# ── Type selection callbacks ──────────────────────────────
@app.on_callback_query(filters.regex("^gs_(pyro2|pyro1|tele)$"))
async def gs_type_cb(client, cq: CallbackQuery):
    uid  = cq.from_user.id
    kind = cq.data.split("_")[1]   # pyro2 | pyro1 | tele
    import time as _t
    _sessions[uid] = {"kind": kind, "step": "phone", "started_at": _t.time()}
    label = {"pyro2": "Pyrogram V2", "pyro1": "Pyrogram V1", "tele": "Telethon"}[kind]
    await cq.answer()
    await cq.edit_message_text(
        f"<emoji id='{E_KEY}'>🔑</emoji> <b>{label} sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ</b>\n\n"
        f"<emoji id='{E_SPARK}'>✨</emoji> <b>sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴᴄʟᴜᴅɪɴɢ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ :</b>\n\n"
        f"<i>ᴇxᴀᴍᴩʟᴇ : +919876543210</i>\n\n"
        f"<emoji id='{E_DIAMOND}'>💎</emoji> <i>ʏᴏᴜʀ ᴘʜᴏɴᴇ ɪs ɴᴇᴠᴇʀ sᴛᴏʀᴇᴅ ʙʏ ᴜs.</i>",
        reply_markup=_markup_cancel(),
    )


@app.on_callback_query(filters.regex("^gs_cancel$"))
async def gs_cancel_cb(client, cq: CallbackQuery):
    uid = cq.from_user.id
    _sessions.pop(uid, None)
    await cq.answer("Cancelled.")
    await cq.edit_message_text(
        f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.</b>"
    )


# ── Message handler for interactive steps ─────────────────
@app.on_message(filters.private & filters.text & ~filters.command([]))
async def gs_step_handler(client, message: Message):
    uid = message.from_user.id
    sess = _sessions.get(uid)
    if not sess:
        return

    step = sess["step"]
    text = message.text.strip()

    # ── STEP 1: phone number ──────────────────────────────
    if step == "phone":
        if not text.startswith("+"):
            return await message.reply_text(
                f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ᴘʟᴇᴀsᴇ ɪɴᴄʟᴜᴅᴇ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ :</b> <code>+91XXXXXXXXXX</code>",
                reply_markup=_markup_cancel(),
            )
        kind = sess["kind"]
        wait = await message.reply_text(
            f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>sᴇɴᴅɪɴɢ OTP ᴛᴏ {text}...</b>"
        )
        try:
            if kind in ("pyro2", "pyro1"):
                tg_client = Client(
                    f":memory:",
                    api_id=_API_ID,
                    api_hash=_API_HASH,
                    in_memory=True,
                )
                await tg_client.connect()
                sent_code = await tg_client.send_code(text)
                sess.update({
                    "step": "otp",
                    "phone": text,
                    "phone_code_hash": sent_code.phone_code_hash,
                    "tg_client": tg_client,
                })
                await wait.edit_text(
                    f"<emoji id='{E_SPARK}'>✨</emoji> <b>OTP sᴇɴᴛ ᴛᴏ {text}!</b>\n\n"
                    f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ OTP ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ :</b>\n"
                    f"<i>ᴇxᴀᴍᴩʟᴇ : <code>12345</code></i>",
                    reply_markup=_markup_cancel(),
                )
            else:
                # Telethon
                try:
                    from telethon.sync import TelegramClient
                    from telethon.sessions import StringSession
                    tele_client = TelegramClient(StringSession(), _API_ID, _API_HASH)
                    await tele_client.connect()
                    sent = await tele_client.send_code_request(text)
                    sess.update({
                        "step": "otp",
                        "phone": text,
                        "phone_code_hash": sent.phone_code_hash,
                        "tg_client": tele_client,
                    })
                    await wait.edit_text(
                        f"<emoji id='{E_SPARK}'>✨</emoji> <b>OTP sᴇɴᴛ ᴛᴏ {text}!</b>\n\n"
                        f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ OTP ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ :</b>",
                        reply_markup=_markup_cancel(),
                    )
                except ImportError:
                    del _sessions[uid]
                    await wait.edit_text(
                        f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>Telethon ɪs ɴᴏᴛ ɪɴsᴛᴀʟʟᴇᴅ.</b>\n"
                        f"ᴜsᴇ Pyrogram V2 ɪɴsᴛᴇᴀᴅ."
                    )
        except Exception as e:
            del _sessions[uid]
            await wait.edit_text(
                f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>\n\n"
                f"ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴡɪᴛʜ /genstring"
            )
        return

    # ── STEP 2: OTP ───────────────────────────────────────
    if step == "otp":
        otp  = text.replace(" ", "")
        kind = sess["kind"]
        wait = await message.reply_text(
            f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ᴠᴇʀɪғʏɪɴɢ OTP...</b>"
        )
        try:
            tg_client = sess["tg_client"]
            if kind in ("pyro2", "pyro1"):
                try:
                    await tg_client.sign_in(
                        sess["phone"], sess["phone_code_hash"], otp
                    )
                except Exception as e:
                    if "PASSWORD" in str(e).upper() or "2FA" in str(e).upper() or "Two" in str(e):
                        sess["step"] = "2fa"
                        return await wait.edit_text(
                            f"<emoji id='{E_KEY}'>🔑</emoji> <b>2FA ᴘᴀssᴡᴏʀᴅ ᴅᴇᴛᴇᴄᴛᴇᴅ!</b>\n\n"
                            f"<b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴛᴡᴏ-ғᴀᴄᴛᴏʀ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ :</b>",
                            reply_markup=_markup_cancel(),
                        )
                    raise e
                string_session = await tg_client.export_session_string()
                await tg_client.disconnect()
            else:
                # Telethon
                from telethon.sessions import StringSession
                await tg_client.sign_in(
                    sess["phone"], code=otp, phone_code_hash=sess["phone_code_hash"]
                )
                string_session = tg_client.session.save()
                await tg_client.disconnect()

            del _sessions[uid]
            label = {"pyro2": "Pyrogram V2", "pyro1": "Pyrogram V1", "tele": "Telethon"}[kind]
            await wait.edit_text(
                f"<emoji id='{E_CROWN}'>👑</emoji> <b>sᴜᴄᴄᴇss! ʏᴏᴜʀ {label} sᴛʀɪɴɢ sᴇssɪᴏɴ :</b>"
            )
            await message.reply_text(
                f"<code>{string_session}</code>\n\n"
                f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ᴋᴇᴇᴘ ᴛʜɪs sᴀғᴇ! ɴᴇᴠᴇʀ sʜᴀʀᴇ ɪᴛ.</b>",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🔑 ɢᴇɴᴇʀᴀᴛᴇ ᴀɴᴏᴛʜᴇʀ",
                        callback_data="gs_restart",
                    ),
                ]]),
            )
        except Exception as e:
            del _sessions[uid]
            await wait.edit_text(
                f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>\n\n"
                f"ᴜsᴇ /genstring ᴛᴏ ᴛʀʏ ᴀɢᴀɪɴ."
            )
        return

    # ── STEP 3: 2FA password ──────────────────────────────
    if step == "2fa":
        wait = await message.reply_text(
            f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ᴠᴇʀɪғʏɪɴɢ 2FA...</b>"
        )
        try:
            tg_client = sess["tg_client"]
            await tg_client.check_password(text)
            string_session = await tg_client.export_session_string()
            await tg_client.disconnect()
            del _sessions[uid]
            await wait.edit_text(
                f"<emoji id='{E_CROWN}'>👑</emoji> <b>sᴜᴄᴄᴇss! ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ :</b>"
            )
            await message.reply_text(
                f"<code>{string_session}</code>\n\n"
                f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ᴋᴇᴇᴘ ᴛʜɪs sᴀғᴇ!</b>"
            )
        except Exception as e:
            del _sessions[uid]
            await wait.edit_text(
                f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴡʀᴏɴɢ ᴩᴀssᴡᴏʀᴅ.</b> <code>{e}</code>"
            )


@app.on_callback_query(filters.regex("^gs_restart$"))
async def gs_restart(client, cq: CallbackQuery):
    await cq.answer()
    uid = cq.from_user.id
    _sessions.pop(uid, None)
    await cq.edit_message_text(
        f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴄʜᴏᴏsᴇ sᴇssɪᴏɴ ᴛʏᴘᴇ :</b>",
        reply_markup=_markup_type(),
    )


# ── Session timeout janitor (runs every 5 min) ────────────
async def _genstring_janitor():
    TIMEOUT = 300  # 5 minutes
    while True:
        await asyncio.sleep(60)
        now = __import__("time").time()
        for uid, sess in list(_sessions.items()):
            if now - sess.get("started_at", now) > TIMEOUT:
                tg = sess.get("tg_client")
                if tg:
                    try:
                        await tg.disconnect()
                    except Exception:
                        pass
                _sessions.pop(uid, None)

asyncio.create_task(_genstring_janitor())
