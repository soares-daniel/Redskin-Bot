import logging
import sys

from discord.ext import commands

from bot.bot import PRDBot


class GeneralEvents(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.bot.file_handler)
        self.logger.addHandler(self.bot.stream_handler)

    @commands.Cog.listener()
    async def on_application_command(self, context) -> None:
        """Log application commands"""
        self.logger.debug(f"Application command: {context.command} - {context.guild} - {context.author}")

    @commands.Cog.listener()
    async def on_application_command_completion(self, context) -> None:
        """Log application commands completion"""
        self.logger.debug(f"Application command completed: {context.command} - {context.guild} - {context.author}")

    @commands.Cog.listener()
    async def on_application_command_error(self, context) -> None:
        """Log application commands error"""
        self.logger.error(f"Application command error: {context.command} - {context.guild} - {context.author}")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs) -> None:
        """Log errors"""
        self.logger.exception(f"Event {event} raised an exception! args: {args} kwargs: {kwargs}",
                              exc_info=sys.exc_info())


def setup(bot) -> None:
    bot.add_cog(GeneralEvents(bot))


