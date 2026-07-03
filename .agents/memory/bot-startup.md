---
name: Bot startup requirement
description: Bot requires STRING_SESSION (Pyrogram assistant account session) env var; without it the bot exits immediately at startup.
---

**Rule:** The bot will not start without at least one of `STRING_SESSION`, `STRING_SESSION2`…`STRING_SESSION5` set as an environment variable.

**Why:** `MADARAMUSIC/__main__.py` checks all five strings and calls `exit()` if none are set. The assistant account (userbot) is required to join voice chats for music streaming.

**How to apply:** The user must generate a Pyrogram string session (via /genstring in the bot's DM once started, or via another session generator) and set it as the `STRING_SESSION` Replit secret. This is a configuration step, not a code fix.
