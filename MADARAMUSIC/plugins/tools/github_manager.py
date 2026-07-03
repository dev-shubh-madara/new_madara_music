# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  💎 GitHub Manager — Full Repository Control    ║
# ╚══════════════════════════════════════════════════╝
import io
import os
import zipfile
import asyncio

import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MADARAMUSIC import app
from MADARAMUSIC.core.mongo import mongodb
from MADARAMUSIC.utils.emojis import (
    E_GLOBE, E_STAR, E_SPARK, E_CLOSE, E_KEY, E_THUNDER,
    E_FIRE, E_GEAR, E_DIAMOND, E_CROWN, E_HEART, E_LOCK,
)

# ── GitHub token per-user store ───────────────────────────
token_db = mongodb["github_tokens"]


async def _get_token(user_id: int) -> str | None:
    doc = await token_db.find_one({"user_id": user_id})
    return doc["token"] if doc else None


async def _set_token(user_id: int, token: str):
    await token_db.update_one(
        {"user_id": user_id},
        {"$set": {"token": token}},
        upsert=True,
    )


def _headers(token: str | None) -> dict:
    h = {"Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


async def _gh_get(url: str, token: str | None) -> dict | list | None:
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=_headers(token)) as r:
            if r.status == 200:
                return await r.json()
            return None


def _nav_buttons():
    return [
        InlineKeyboardButton("🏠 Menu", callback_data="gh_menu",
),
        InlineKeyboardButton("✖️ Close", callback_data="gh_close",
),
    ]


def _main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 ᴜsᴇʀ ɪɴғᴏ", callback_data="gh_help_user",
),
            InlineKeyboardButton("📦 ʀᴇᴩᴏ ɪɴғᴏ", callback_data="gh_help_repo",
),
        ],
        [
            InlineKeyboardButton("⬇️ ᴅᴏᴡɴʟᴏᴀᴅ ᴢɪᴘ", callback_data="gh_help_zip",
),
            InlineKeyboardButton("⬆️ ᴜᴘʟᴏᴀᴅ ᴢɪᴘ", callback_data="gh_help_push",
),
        ],
        [
            InlineKeyboardButton("🔖 ɪssᴜᴇs", callback_data="gh_help_issues",
),
            InlineKeyboardButton("📝 ᴄᴏᴍᴍɪᴛs", callback_data="gh_help_commits",
),
        ],
        [
            InlineKeyboardButton("⭐ sᴛᴀʀ ʀᴇᴩᴏ", callback_data="gh_help_star",
),
            InlineKeyboardButton("🍴 ғᴏʀᴋ ʀᴇᴩᴏ", callback_data="gh_help_fork",
),
        ],
        [
            InlineKeyboardButton("🌿 ʙʀᴀɴᴄʜᴇs", callback_data="gh_help_branches",
),
            InlineKeyboardButton("🔑 sᴇᴛ ᴛᴏᴋᴇɴ", callback_data="gh_help_token",
),
        ],
        [
            InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="gh_close",
),
        ],
    ])


# ── /github — main menu ────────────────────────────────────
@app.on_message(filters.command(["github", "gh", "gitmanager"]))
async def github_menu(client, message: Message):
    await message.reply_text(
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ɢɪᴛʜᴜʙ ᴍᴀɴᴀɢᴇʀ</b>\n\n"
        f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs :</b>\n\n"
        f"• /gitinfo <code>username</code>\n"
        f"• /gitrepo <code>owner/repo</code>\n"
        f"• /zrepo <code>owner/repo</code> [token]\n"
        f"• /zpush <code>owner/repo</code> <code>token</code> (reply to ZIP)\n"
        f"• /gitissues <code>owner/repo</code>\n"
        f"• /gitcommits <code>owner/repo</code>\n"
        f"• /gitstar <code>owner/repo</code>\n"
        f"• /gitfork <code>owner/repo</code>\n"
        f"• /gitbranch <code>owner/repo</code>\n"
        f"• /gittoken <code>your_token</code>\n\n"
        f"<emoji id='{E_SPARK}'>✨</emoji> <i>sᴇᴛ ᴛᴏᴋᴇɴ ᴏɴᴄᴇ ᴛᴏ ᴀᴄᴄᴇss ᴩʀɪᴠᴀᴛᴇ ʀᴇᴩᴏs.</i>",
        reply_markup=_main_menu(),
    )


@app.on_callback_query(filters.regex("^gh_menu$"))
async def gh_menu_cb(client, cq):
    await cq.answer()
    await cq.edit_message_text(
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ɢɪᴛʜᴜʙ ᴍᴀɴᴀɢᴇʀ</b>",
        reply_markup=_main_menu(),
    )


@app.on_callback_query(filters.regex("^gh_close$"))
async def gh_close_cb(client, cq):
    await cq.answer()
    await cq.message.delete()


@app.on_callback_query(filters.regex("^gh_help_"))
async def gh_help_cb(client, cq):
    await cq.answer()
    helps = {
        "gh_help_user":    "/gitinfo <code>username</code> — ɢᴇᴛ ɢɪᴛʜᴜʙ ᴜsᴇʀ ᴘʀᴏғɪʟᴇ",
        "gh_help_repo":    "/gitrepo <code>owner/repo</code> — ɢᴇᴛ ʀᴇᴩᴏ ɪɴғᴏ",
        "gh_help_zip":     "/zrepo <code>owner/repo</code> [token] — ᴅᴏᴡɴʟᴏᴀᴅ ᴢɪᴘ",
        "gh_help_push":    "/zpush <code>owner/repo</code> <code>token</code> (ʀᴇᴩʟʏ ᴛᴏ ᴢɪᴩ) — ᴜᴘʟᴏᴀᴅ",
        "gh_help_issues":  "/gitissues <code>owner/repo</code> — ʟɪsᴛ ɪssᴜᴇs",
        "gh_help_commits": "/gitcommits <code>owner/repo</code> — ʀᴇᴄᴇɴᴛ ᴄᴏᴍᴍɪᴛs",
        "gh_help_star":    "/gitstar <code>owner/repo</code> — sᴛᴀʀ ᴀ ʀᴇᴩᴏ",
        "gh_help_fork":    "/gitfork <code>owner/repo</code> — ғᴏʀᴋ ᴀ ʀᴇᴩᴏ",
        "gh_help_branches":"/gitbranch <code>owner/repo</code> — ʟɪsᴛ ʙʀᴀɴᴄʜᴇs",
        "gh_help_token":   "/gittoken <code>your_token</code> — sᴀᴠᴇ ʏᴏᴜʀ ɢɪᴛʜᴜʙ ᴛᴏᴋᴇɴ",
    }
    await cq.edit_message_text(
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ᴄᴏᴍᴍᴀɴᴅ ɪɴғᴏ :</b>\n\n{helps.get(cq.data, '')}",
        reply_markup=InlineKeyboardMarkup([_nav_buttons()]),
    )


# ── /gittoken ─────────────────────────────────────────────
@app.on_message(filters.command("gittoken") & filters.private)
async def cmd_gittoken(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_KEY}'>🔑</emoji> <b>ᴜsᴀɢᴇ :</b> /gittoken <code>your_github_token</code>"
        )
    token = message.command[1]
    await _set_token(message.from_user.id, token)
    try:
        await message.delete()
    except Exception:
        pass
    await message.reply_text(
        f"<emoji id='{E_LOCK}'>🔒</emoji> <b>ɢɪᴛʜᴜʙ ᴛᴏᴋᴇɴ sᴀᴠᴇᴅ sᴇᴄᴜʀᴇʟʏ!</b>\n"
        f"<i>ᴜsᴇ /gittoken ɪɴ PM ᴏɴʟʏ ғᴏʀ sᴇᴄᴜʀɪᴛʏ.</i>"
    )


@app.on_message(filters.command("gittoken") & ~filters.private)
async def cmd_gittoken_group(client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    await message.reply_text(
        f"<emoji id='{E_LOCK}'>🔒</emoji> <b>ᴅᴏ ɴᴏᴛ ᴜsᴇ ᴛᴏᴋᴇɴs ɪɴ ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴩs!</b>\n"
        f"<i>sᴇᴛ ʏᴏᴜʀ ᴛᴏᴋᴇɴ ɪɴ ᴍʏ DM.</i>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔑 sᴇᴛ ᴛᴏᴋᴇɴ ɪɴ DM",
                url=f"https://t.me/{app.username}",
            ),
        ]]),
    )


# ── /gitinfo ──────────────────────────────────────────────
@app.on_message(filters.command("gitinfo"))
async def cmd_gitinfo(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_STAR}'>⭐</emoji> <b>ᴜsᴀɢᴇ :</b> /gitinfo <code>username</code>"
        )
    username = message.command[1]
    wait = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴇᴛᴄʜɪɴɢ...</b>")
    token = await _get_token(message.from_user.id)
    data  = await _gh_get(f"https://api.github.com/users/{username}", token)
    if not data:
        return await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ :</b> <code>{username}</code>")
    await wait.edit_text(
        f"<emoji id='{E_STAR}'>⭐</emoji> <b>ɢɪᴛʜᴜʙ ᴜsᴇʀ :</b> <a href='{data['html_url']}'>{data['login']}</a>\n\n"
        f"<emoji id='{E_CROWN}'>👑</emoji> <b>ɴᴀᴍᴇ :</b> {data.get('name') or 'N/A'}\n"
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʙɪᴏ :</b> {data.get('bio') or 'N/A'}\n"
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʟᴏᴄᴀᴛɪᴏɴ :</b> {data.get('location') or 'N/A'}\n"
        f"<emoji id='{E_FIRE}'>🔥</emoji> <b>ʀᴇᴩᴏs :</b> {data.get('public_repos', 0)}\n"
        f"<emoji id='{E_HEART}'>❤️</emoji> <b>ғᴏʟʟᴏᴡᴇʀs :</b> {data.get('followers', 0)}\n"
        f"<emoji id='{E_SPARK}'>✨</emoji> <b>ғᴏʟʟᴏᴡɪɴɢ :</b> {data.get('following', 0)}\n"
        f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ᴊᴏɪɴᴇᴅ :</b> {data.get('created_at', '')[:10]}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🌐 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ",
                url=data["html_url"],
            ),
        ]]),
    )


# ── /gitrepo ──────────────────────────────────────────────
@app.on_message(filters.command("gitrepo"))
async def cmd_gitrepo(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ᴜsᴀɢᴇ :</b> /gitrepo <code>owner/repo</code>"
        )
    repo  = message.command[1]
    wait  = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴇᴛᴄʜɪɴɢ...</b>")
    token = await _get_token(message.from_user.id)
    data  = await _gh_get(f"https://api.github.com/repos/{repo}", token)
    if not data:
        return await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ʀᴇᴩᴏ ɴᴏᴛ ғᴏᴜɴᴅ :</b> <code>{repo}</code>")
    await wait.edit_text(
        f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʀᴇᴩᴏ :</b> <a href='{data['html_url']}'>{data['full_name']}</a>\n\n"
        f"<emoji id='{E_SPARK}'>✨</emoji> <b>ᴅᴇsᴄ :</b> {data.get('description') or 'N/A'}\n"
        f"<emoji id='{E_STAR}'>⭐</emoji> <b>sᴛᴀʀs :</b> {data.get('stargazers_count', 0)}\n"
        f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ғᴏʀᴋs :</b> {data.get('forks_count', 0)}\n"
        f"<emoji id='{E_FIRE}'>🔥</emoji> <b>ᴏᴩᴇɴ ɪssᴜᴇs :</b> {data.get('open_issues_count', 0)}\n"
        f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ʟᴀɴɢᴜᴀɢᴇ :</b> {data.get('language') or 'N/A'}\n"
        f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ᴅᴇғᴀᴜʟᴛ ʙʀᴀɴᴄʜ :</b> {data.get('default_branch', 'main')}\n"
        f"<emoji id='{E_CROWN}'>👑</emoji> <b>ʟɪᴄᴇɴsᴇ :</b> {(data.get('license') or {}).get('spdx_id', 'N/A')}\n"
        f"<emoji id='{E_LOCK}'>🔒</emoji> <b>ᴘʀɪᴠᴀᴛᴇ :</b> {'Yes' if data.get('private') else 'No'}\n"
        f"<emoji id='{E_HEART}'>❤️</emoji> <b>ᴜᴘᴅᴀᴛᴇᴅ :</b> {data.get('updated_at', '')[:10]}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🌐 ᴏᴩᴇɴ", url=data["html_url"],
),
            InlineKeyboardButton("⬇️ ZIP", callback_data=f"gh_zip_{repo}",
),
        ]]),
    )


# ── /zrepo — download repo as ZIP ─────────────────────────
@app.on_message(filters.command("zrepo"))
async def cmd_zrepo(client, message: Message):
    args = message.command[1:]
    if not args:
        return await message.reply_text(
            f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ᴜsᴀɢᴇ :</b> /zrepo <code>owner/repo</code> [token]"
        )
    repo  = args[0]
    token = args[1] if len(args) > 1 else await _get_token(message.from_user.id)
    await _do_zrepo(message, repo, token)


@app.on_callback_query(filters.regex("^gh_zip_"))
async def gh_zip_cb(client, cq):
    await cq.answer()
    repo  = cq.data[7:]
    token = await _get_token(cq.from_user.id)
    await _do_zrepo(cq.message, repo, token, edit=False)


async def _do_zrepo(msg, repo: str, token: str | None, edit=False):
    wait = await msg.reply_text(
        f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ <code>{repo}</code> ᴀs ZIP...</b>"
    )
    headers = _headers(token)
    url     = f"https://api.github.com/repos/{repo}/zipball"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers, allow_redirects=True) as r:
                if r.status != 200:
                    return await wait.edit_text(
                        f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ :</b> {r.status}. Make sure repo is public or token is valid."
                    )
                data = await r.read()
        os.makedirs("downloads", exist_ok=True)
        fname = f"downloads/{repo.replace('/', '_')}.zip"
        with open(fname, "wb") as f:
            f.write(data)
        size_mb = len(data) / (1024 * 1024)
        await wait.edit_text(
            f"<emoji id='{E_THUNDER}'>⚡</emoji> <b>ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ! sɪᴢᴇ : {size_mb:.2f} MB — sᴇɴᴅɪɴɢ...</b>"
        )
        await msg.reply_document(
            fname,
            caption=(
                f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʀᴇᴩᴏ :</b> <code>{repo}</code>\n"
                f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>sɪᴢᴇ :</b> {size_mb:.2f} MB"
            ),
        )
        await wait.delete()
        try:
            os.remove(fname)
        except Exception:
            pass
    except Exception as e:
        await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")


# ── /zpush — upload ZIP to repo ───────────────────────────
@app.on_message(filters.command("zpush"))
async def cmd_zpush(client, message: Message):
    # Token must NOT be passed publicly — use stored token or DM-only
    if len(message.command) >= 3 and not (hasattr(message, "chat") and message.chat.type.name == "PRIVATE"):
        try:
            await message.delete()
        except Exception:
            pass
        return await message.reply_text(
            f"<emoji id='{E_LOCK}'>🔒</emoji> <b>ᴅᴏ ɴᴏᴛ ᴩᴀss ᴛᴏᴋᴇɴs ɪɴ ᴩᴜʙʟɪᴄ!</b>\n"
            f"sᴇᴛ ʏᴏᴜʀ ᴛᴏᴋᴇɴ ᴡɪᴛʜ /gittoken ɪɴ ᴅᴍ, ᴛʜᴇɴ ᴜsᴇ /zpush <code>owner/repo</code>"
        )
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_FIRE}'>🔥</emoji> <b>ᴜsᴀɢᴇ :</b> /zpush <code>owner/repo</code>\n"
            f"<i>ʀᴇᴩʟʏ ᴛᴏ ᴀ ZIP ғɪʟᴇ. sᴇᴛ ᴛᴏᴋᴇɴ ᴡɪᴛʜ /gittoken ɪɴ DM ғɪʀsᴛ.</i>"
        )
    repo  = message.command[1]
    token = await _get_token(message.from_user.id)
    if not token:
        return await message.reply_text(
            f"<emoji id='{E_KEY}'>🔑</emoji> <b>sᴇᴛ ʏᴏᴜʀ ɢɪᴛʜᴜʙ ᴛᴏᴋᴇɴ ғɪʀsᴛ :</b> /gittoken <code>your_token</code> (ɪɴ DM)"
        )
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text(
            f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ʀᴇᴩʟʏ ᴛᴏ ᴀ ZIP ᴅᴏᴄᴜᴍᴇɴᴛ ᴛᴏ ᴜᴩʟᴏᴀᴅ ɪᴛ.</b>"
        )
    wait = await message.reply_text(
        f"<emoji id='{E_FIRE}'>🔥</emoji> <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴢɪᴩ...</b>"
    )
    try:
        zip_path = await app.download_media(
            message.reply_to_message.document.file_id,
            file_name=f"downloads/zpush_{repo.replace('/', '_')}.zip",
        )
        await wait.edit_text(
            f"<emoji id='{E_FIRE}'>🔥</emoji> <b>ᴇxᴛʀᴀᴄᴛɪɴɢ & ᴜᴩʟᴏᴀᴅɪɴɢ ᴛᴏ {repo}...</b>"
        )
        import base64
        headers = _headers(token)
        headers["Content-Type"] = "application/json"

        with zipfile.ZipFile(zip_path, "r") as zf:
            files = [n for n in zf.namelist() if not n.endswith("/")]

        uploaded = 0
        errors   = 0
        async with aiohttp.ClientSession() as s:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for fname in files[:50]:   # limit 50 files per push
                    content = base64.b64encode(zf.read(fname)).decode()
                    # strip the first directory component
                    parts    = fname.split("/", 1)
                    rel_path = parts[1] if len(parts) > 1 else fname
                    api_url  = f"https://api.github.com/repos/{repo}/contents/{rel_path}"
                    # check if file exists
                    async with s.get(api_url, headers=_headers(token)) as r:
                        sha = (await r.json()).get("sha") if r.status == 200 else None
                    payload = {
                        "message": f"Upload via MADARA MUSIC Bot: {rel_path}",
                        "content": content,
                    }
                    if sha:
                        payload["sha"] = sha
                    async with s.put(api_url, json=payload, headers=headers) as r:
                        if r.status in (200, 201):
                            uploaded += 1
                        else:
                            errors += 1

        await wait.edit_text(
            f"<emoji id='{E_CROWN}'>👑</emoji> <b>ᴜᴩʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
            f"<emoji id='{E_STAR}'>⭐</emoji> <b>ᴜᴩʟᴏᴀᴅᴇᴅ :</b> {uploaded} ғɪʟᴇs\n"
            f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴇʀʀᴏʀs :</b> {errors}\n"
            f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʀᴇᴩᴏ :</b> https://github.com/{repo}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🌐 ᴠɪᴇᴡ ʀᴇᴩᴏ",
                                     url=f"https://github.com/{repo}",
),
            ]]),
        )
        try:
            os.remove(zip_path)
        except Exception:
            pass
    except Exception as e:
        await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")


# ── /gitissues ────────────────────────────────────────────
@app.on_message(filters.command("gitissues"))
async def cmd_gitissues(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_SPARK}'>✨</emoji> <b>ᴜsᴀɢᴇ :</b> /gitissues <code>owner/repo</code>"
        )
    repo  = message.command[1]
    wait  = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴇᴛᴄʜɪɴɢ...</b>")
    token = await _get_token(message.from_user.id)
    data  = await _gh_get(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=10", token)
    if data is None:
        return await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ɪssᴜᴇs.</b>")
    text = f"<emoji id='{E_SPARK}'>✨</emoji> <b>ᴏᴩᴇɴ ɪssᴜᴇs — {repo}</b>\n\n"
    if not data:
        text += "<i>No open issues! 🎉</i>"
    for i in data[:10]:
        text += f"• <a href='{i['html_url']}'>#{i['number']}</a> {i['title'][:60]}\n"
    await wait.edit_text(text, disable_web_page_preview=True)


# ── /gitcommits ───────────────────────────────────────────
@app.on_message(filters.command("gitcommits"))
async def cmd_gitcommits(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ᴜsᴀɢᴇ :</b> /gitcommits <code>owner/repo</code>"
        )
    repo  = message.command[1]
    wait  = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴇᴛᴄʜɪɴɢ...</b>")
    token = await _get_token(message.from_user.id)
    data  = await _gh_get(f"https://api.github.com/repos/{repo}/commits?per_page=10", token)
    if data is None:
        return await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ.</b>")
    text = f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ʀᴇᴄᴇɴᴛ ᴄᴏᴍᴍɪᴛs — {repo}</b>\n\n"
    for c in data[:10]:
        sha     = c["sha"][:7]
        msg_txt = c["commit"]["message"].split("\n")[0][:60]
        author  = c["commit"]["author"]["name"][:15]
        text   += f"• <code>{sha}</code> {msg_txt} — <i>{author}</i>\n"
    await wait.edit_text(text, disable_web_page_preview=True)


# ── /gitstar ──────────────────────────────────────────────
@app.on_message(filters.command("gitstar"))
async def cmd_gitstar(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_STAR}'>⭐</emoji> <b>ᴜsᴀɢᴇ :</b> /gitstar <code>owner/repo</code>"
        )
    repo  = message.command[1]
    token = await _get_token(message.from_user.id)
    if not token:
        return await message.reply_text(
            f"<emoji id='{E_KEY}'>🔑</emoji> <b>sᴇᴛ ᴛᴏᴋᴇɴ ғɪʀsᴛ :</b> /gittoken <code>your_token</code>"
        )
    async with aiohttp.ClientSession() as s:
        async with s.put(
            f"https://api.github.com/user/starred/{repo}",
            headers=_headers(token),
        ) as r:
            if r.status == 204:
                await message.reply_text(
                    f"<emoji id='{E_STAR}'>⭐</emoji> <b>ᴡᴏᴡ! ʏᴏᴜ sᴛᴀʀʀᴇᴅ :</b> <code>{repo}</code>"
                )
            else:
                await message.reply_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ :</b> {r.status}")


# ── /gitfork ──────────────────────────────────────────────
@app.on_message(filters.command("gitfork"))
async def cmd_gitfork(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_DIAMOND}'>💎</emoji> <b>ᴜsᴀɢᴇ :</b> /gitfork <code>owner/repo</code>"
        )
    repo  = message.command[1]
    token = await _get_token(message.from_user.id)
    if not token:
        return await message.reply_text(
            f"<emoji id='{E_KEY}'>🔑</emoji> <b>sᴇᴛ ᴛᴏᴋᴇɴ ғɪʀsᴛ :</b> /gittoken <code>your_token</code>"
        )
    wait = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴏʀᴋɪɴɢ {repo}...</b>")
    async with aiohttp.ClientSession() as s:
        async with s.post(
            f"https://api.github.com/repos/{repo}/forks",
            headers=_headers(token),
        ) as r:
            if r.status in (200, 202):
                d = await r.json()
                await wait.edit_text(
                    f"<emoji id='{E_CROWN}'>👑</emoji> <b>ғᴏʀᴋᴇᴅ!</b>\n"
                    f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʏᴏᴜʀ ғᴏʀᴋ :</b> <a href='{d['html_url']}'>{d['full_name']}</a>"
                )
            else:
                await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ :</b> {r.status}")


# ── /gitbranch ────────────────────────────────────────────
@app.on_message(filters.command("gitbranch"))
async def cmd_gitbranch(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ᴜsᴀɢᴇ :</b> /gitbranch <code>owner/repo</code>"
        )
    repo  = message.command[1]
    wait  = await message.reply_text(f"<emoji id='{E_GEAR}'>⚙️</emoji> <b>ғᴇᴛᴄʜɪɴɢ...</b>")
    token = await _get_token(message.from_user.id)
    data  = await _gh_get(f"https://api.github.com/repos/{repo}/branches?per_page=20", token)
    if data is None:
        return await wait.edit_text(f"<emoji id='{E_CLOSE}'>✖️</emoji> <b>ғᴀɪʟᴇᴅ.</b>")
    text  = f"<emoji id='{E_GLOBE}'>🌐</emoji> <b>ʙʀᴀɴᴄʜᴇs — {repo}</b>\n\n"
    for b in data:
        text += f"🌿 <code>{b['name']}</code>\n"
    await wait.edit_text(text)
