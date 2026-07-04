# MADARA MUSIC Bot

A feature-rich Telegram music & entertainment bot built with Python, Pyrogram, py-tgcalls, and MongoDB.

## Stack
- **Python 3.11**
- **Pyrogram** (pyrofork fork) — Telegram client
- **py-tgcalls** — voice/video call streaming
- **MongoDB Atlas** — database (via Motor async driver)
- **yt-dlp / spotipy** — music platform integrations

## How to run

```
pip install -r requirements.txt -q && python3 -m MADARAMUSIC
```

## Required environment variables

| Variable | Description |
|---|---|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `OWNER_ID` | Your Telegram user ID (integer) |
| `LOGGER_ID` | Telegram group/channel ID for bot logs (bot must be admin) |
| `STRING_SESSION` | Pyrogram session string for the assistant userbot |

## Optional environment variables

| Variable | Description |
|---|---|
| `STRING_SESSION2`–`STRING_SESSION7` | Extra assistant session strings |
| `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` | Spotify API credentials |
| `HEROKU_API_KEY` / `HEROKU_APP_NAME` | Heroku integration |
| `GIT_TOKEN` | GitHub token |
| `OWNER_USERNAME` | Your Telegram username |
| `BOT_USERNAME` | Bot username |
| `LOGGER_ID` | Log group/channel ID |
| `DURATION_LIMIT` | Max stream duration in minutes (default: 17000) |

## Project structure

```
MADARAMUSIC/
├── core/           # Bot core (client, mongo, userbot, git)
├── platforms/      # Music platform handlers (YouTube, Spotify, etc.)
├── plugins/        # Command handlers (admins, bot, extra, misc, sudo, tools)
├── utils/          # Database helpers, decorators, inline keyboards, thumbnails
├── assets/         # Images and fonts
└── __main__.py     # Entry point
config.py           # Config loaded from environment variables
strings/            # Language files (YAML)
```

## User preferences
