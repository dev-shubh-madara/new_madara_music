# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  The Most Powerful Telegram Music Bot            ║
# ║  Built with ❤️ for music lovers everywhere       ║
# ╚══════════════════════════════════════════════════╝
from pyrogram import Client
import config
from ..logging import LOGGER
assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="SHUKLAAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="SHUKLAAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="SHUKLAAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="SHUKLAAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="SHUKLAAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def _start_one(self, client, slot: int, name: str):
        """Start a single assistant, skipping gracefully on auth errors."""
        try:
            await client.start()
        except Exception as e:
            LOGGER(__name__).warning(
                f"Assistant {name} failed to start ({type(e).__name__}: {e}). "
                "Update STRING_SESSION env var with a fresh Pyrogram session string."
            )
            # Clean up to avoid unclosed-session resource leaks
            try:
                await client.stop()
            except Exception:
                pass
            return
        try:
            await client.join_chat("ITSZSHUKLA")
        except:
            pass
        try:
            await client.join_chat("MASTIWITHFRIENDSXD")
        except:
            pass
        assistants.append(slot)
        try:
            await client.send_message(config.LOGGER_ID, f"Assistant {name} Started")
        except:
            LOGGER(__name__).warning(
                f"Assistant {name} cannot reach log group — add it as admin in your log group."
            )
        client.id = client.me.id
        client.name = client.me.mention
        client.username = client.me.username
        assistantids.append(client.id)
        LOGGER(__name__).info(f"Assistant {name} Started as {client.name}")

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        if config.STRING1:
            await self._start_one(self.one, 1, "One")
        if config.STRING2:
            await self._start_one(self.two, 2, "Two")
        if config.STRING3:
            await self._start_one(self.three, 3, "Three")
        if config.STRING4:
            await self._start_one(self.four, 4, "Four")
        if config.STRING5:
            await self._start_one(self.five, 5, "Five")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass