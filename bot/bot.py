import logging
from logging import handlers

from discord import Activity, ActivityType, Intents, ApplicationCommand
from discord.ext import commands


class PRDBot(commands.Bot):
    """The PRD Discord bot."""

    def __init__(self) -> None:
        # Bot
        activity = Activity(type=ActivityType.watching, name="Kalendar")
        intents = Intents.all()
        super().__init__(activity=activity, command_prefix="!", intents=intents)
        # Logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        file_handler = handlers.TimedRotatingFileHandler(
            filename="logs/discord.log", when="midnight", backupCount=7
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(name)s - %(funcName)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        self.file_handler = file_handler
        self.stream_handler = stream_handler
        self.logger = logger

    async def on_ready(self) -> None:
        print("------")
        print("Les Peaux Rouges - Discord Bot")
        print(self.user.name)
        print("------")

        # Get channel with id 1121177566775095478
        channel = self.get_channel(1121177566775095478)
        await channel.send("I fucked your wife")
