from discord.ext import commands
from utils.bot_logger import bot_logger

import os
import logging
import discord
import asyncio
import aiohttp

# discord events logged in a logfile
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.DEBUG)
discord_logger_handler = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="w"
)
discord_logger_handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
discord_logger.addHandler(discord_logger_handler)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="{bot_prefix}", *args, **kwargs)
        self.ignored_cogs = []
        self.loop.create_task(self.startup())

    def _load_cogs(self):
        """Loads cogs from the cogs directory"""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                if filename[:-3] in self.ignored_cogs:
                    continue
                self.load_extension(f"cogs.{filename[:-3]}")
                bot_logger.info(f"Loaded cog: {filename}")

    async def _init_db(self):
        """Initializes database"""
        # If needed, you can setup your DB here
        # bot_logger.info("Initialized DB.")
        pass

    async def startup(self):
        """Simple task that runs on startup. Useful for loading cogs and setting up db."""
        await self.wait_until_ready()

        bot_logger.info(f"{self.user.name} connected to discord!")

        self._load_cogs()
        await self._init_db()

        self.aio_session = aiohttp.ClientSession()


if __name__ == "__main__":
    bot = Bot()

    bot.run(os.getenv("DISCORD_TOKEN"))
