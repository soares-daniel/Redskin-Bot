import logging

from discord.ext import commands

from bot.bot import PRDBot
from bot.views.event import EventSelect
from settings import EVENT_CHANNEL_NAME


class Event(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot
        self.persistent_added = False
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.bot.file_handler)
        self.logger.addHandler(self.bot.stream_handler)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Add persistent views on startup"""
        # Check event channel
        event_channel = await self.bot.fetch_channel(self.bot.EVENT_CHANNEL_ID)
        if not event_channel:
            self.logger.info("Event channel not found. Creating one...")
            guild = self.bot.MAIN_GUILD
            category = self.bot.CATEGORY
            event_channel = await guild.create_text_channel(name=EVENT_CHANNEL_NAME, category=category)
            self.bot.EVENT_CHANNEL_ID = event_channel.id
            self.logger.info("Event channel created.")

        # Check event select menu
        last_message = await event_channel.history(limit=1).flatten()
        if not last_message:
            event_select = EventSelect(self.bot, logger=self.logger)
            await event_select.build()
            await event_channel.send(content="", view=event_select)
            self.logger.info("Event select menu added.")

        # Add persistent view
        if not self.persistent_added:
            self.bot.add_view(EventSelect(self.bot, logger=self.logger))
            self.persistent_added = True
            self.logger.info("Persistent view added.")


def setup(bot) -> None:
    bot.add_cog(Event(bot))
