<div align="center">

<img src="https://files.catbox.moe/5go4t6.jpg" width="200px" style="border-radius: 50%;" alt="MADARA MUSIC"/>

# 🎵 MADARA MUSIC BOT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pyrogram-2.x-red?style=for-the-badge&logo=telegram&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

<p align="center">
  <b>The Most Powerful & Feature-Rich Telegram Music Bot</b><br/>
  Stream music · Fight · Pay · Track Crypto · Manage GitHub — all in one bot.
</p>

<p align="center">
  <a href="https://t.me/YourSupportChat"><img src="https://img.shields.io/badge/Support-Telegram-2CA5E0?style=flat-square&logo=telegram"/></a>
  <a href="https://t.me/YourChannel"><img src="https://img.shields.io/badge/Channel-Updates-2CA5E0?style=flat-square&logo=telegram"/></a>
  <img src="https://img.shields.io/github/stars/ragini19854-prog/new_madara_music?style=flat-square&color=yellow"/>
  <img src="https://img.shields.io/github/forks/ragini19854-prog/new_madara_music?style=flat-square&color=blue"/>
</p>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎵 Music Streaming
- High-quality audio & video streaming
- YouTube, Spotify, Apple Music, SoundCloud
- Queue management with shuffle & loop
- Speed control & volume slider
- Spotify-style animated thumbnails

</td>
<td width="50%">

### 🎮 Entertainment
- **ChatFight** — Word, emoji & flag games with leaderboard
- **Cricket** — Live score updates
- **Couples** — Daily couple pairing game
- **AFK** — Auto away-from-keyboard status

</td>
</tr>
<tr>
<td width="50%">

### 💳 Payments & Crypto
- **UPI Pay** — Generate QR codes for any UPI ID
- **TON Price** — Live TON coin prices (USD & INR)
- **USDT** — Tether live prices
- **TON Balance** — Check any wallet balance

</td>
<td width="50%">

### 🔐 Tools & Utilities
- **GenString** — Pyrogram v1/v2 & Telethon session generator
- **GitHub Manager** — Full GitHub integration with token auth
- **Welcome Cards** — Custom animated welcome images
- **Thumbnails** — Spotify-style music thumbnails

</td>
</tr>
<tr>
<td width="50%">

### 👑 Admin & Moderation
- Auth user system
- Ban, mute, unban all
- Chat blacklist / whitelist
- Broadcast to all chats
- Auto-leaving assistant

</td>
<td width="50%">

### 🌐 Developer Tools
- GitHub repo info, commits, issues, star/fork
- WHOIS domain lookup
- Instagram downloader
- GPT integration
- Reverse image search

</td>
</tr>
</table>

---

## 🚀 Deploy

### Prerequisites
- Python 3.11+
- MongoDB Atlas (free tier works)
- Telegram API credentials

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `API_ID` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | ✅ | From [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | ✅ | MongoDB connection string |
| `OWNER_ID` | ✅ | Your Telegram user ID |
| `STRING_SESSION` | ✅ | Pyrogram v2 string session |
| `LOGGER_ID` | ⚡ | Log channel/group ID |
| `OWNER_USERNAME` | ⚡ | Your Telegram username |
| `BOT_USERNAME` | ⚡ | Bot's username |
| `SUPPORT_CHAT` | ⚡ | Support group URL |
| `SUPPORT_CHANNEL` | ⚡ | Channel URL |
| `SPOTIFY_CLIENT_ID` | 🔵 | Spotify developer app ID |
| `SPOTIFY_CLIENT_SECRET` | 🔵 | Spotify developer secret |
| `STRING_SESSION2–7` | 🔵 | Additional assistant sessions |

> ✅ Required &nbsp; ⚡ Recommended &nbsp; 🔵 Optional

### Quick Start

```bash
# Clone the repository
git clone https://github.com/ragini19854-prog/new_madara_music
cd new_madara_music

# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy .env.example)
cp .env.example .env
# Edit .env with your values

# Start the bot
python3 -m MADARAMUSIC
```

---

## 📋 Commands

### 🎵 Music
| Command | Description |
|---|---|
| `/play [song]` | Stream a song in voice chat |
| `/vplay [song]` | Stream a video |
| `/pause` / `/resume` | Pause or resume playback |
| `/skip` | Skip to next track |
| `/stop` | Stop and clear queue |
| `/queue` | View current queue |
| `/shuffle` | Shuffle the queue |
| `/loop` | Toggle loop mode |
| `/speed` | Adjust playback speed |

### 💳 UPI & Payments
| Command | Description |
|---|---|
| `/setupi [upi@bank]` | Save your UPI ID |
| `/gen [amount]` | Generate a QR code (expires in 10 min) |

### ⚡ Crypto
| Command | Description |
|---|---|
| `/ton` | Live TON price |
| `/usdt` | Live USDT price |
| `/balance [address]` | Check TON wallet balance |

### 🔐 Session Generator
| Command | Description |
|---|---|
| `/genstring` | Generate Pyrogram/Telethon session (PM only) |

### 🌐 GitHub
| Command | Description |
|---|---|
| `/gittoken [token]` | Save your GitHub token |
| `/gitinfo [user]` | GitHub profile info |
| `/gitrepo [user/repo]` | Repository info |
| `/zrepo [user/repo]` | Download repo as ZIP |
| `/zpush [user/repo]` | Push file to repo |
| `/gitissues [user/repo]` | List open issues |
| `/gitcommits [user/repo]` | Recent commits |
| `/gitstar [user/repo]` | Star a repository |
| `/gitfork [user/repo]` | Fork a repository |
| `/gitbranch [user/repo]` | List branches |

### 🎮 Games
| Command | Description |
|---|---|
| `/chatfight` | Start a word/emoji/flag game |
| `/gametop` | View game leaderboard |

---

## 🏗️ Project Structure

```
MADARAMUSIC/
├── core/           # Bot core (client, mongo, git)
├── platforms/      # Music platform handlers (YouTube, Spotify, etc.)
├── plugins/
│   ├── admins/     # Admin commands
│   ├── bot/        # Core bot handlers (start, help, settings)
│   ├── extra/      # Extra tools
│   ├── misc/       # Miscellaneous (filters, notes)
│   ├── sudo/       # Sudo/owner commands
│   └── tools/      # User tools (UPI, Crypto, ChatFight, GitHub...)
├── utils/
│   ├── database/   # MongoDB helpers
│   ├── decorators/ # Language & auth decorators
│   ├── inline/     # Inline keyboard builders
│   ├── emojis.py   # Premium emoji IDs
│   └── thumbnails.py # Spotify-style thumbnail generator
├── assets/         # Images (backgrounds, welcome card, etc.)
└── __main__.py     # Entry point
strings/
├── langs/          # Language files (en.yml, etc.)
└── helpers.py      # Help text strings
```

---

## 🛡️ License

```
Copyright © 2024 MADARA MUSIC
Built with ❤️ for music lovers everywhere.
Open for educational and non-commercial use only.
```

---

<div align="center">

**Made with ❤️ | Star ⭐ this repo if you like it!**

[![Telegram](https://img.shields.io/badge/Join-Telegram-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/YourSupportChat)

</div>
