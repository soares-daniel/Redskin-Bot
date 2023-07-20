import discord
from discord.ext import commands

from bot.bot import PRDBot
from bot.embeds.calendar import CalendarEmbed
from bot.requests.event import get_events


class Calendar(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot

    @commands.slash_command(name="calendar", description="Get the calendar")
    async def calendar(self, ctx: discord.ApplicationContext):
        """Get the calendar"""
        await ctx.respond("Getting calendar...")
        events = await get_events(self.bot.http_client)
        embed = await CalendarEmbed(events=events).build()
        channel = await self.bot.fetch_channel(self.bot.CALENDAR_CHANNEL_ID)
        if channel is None:
            return

        # Get the last message
        last_message = await channel.history(limit=1).flatten()
        if last_message:
            await last_message[0].edit(embed=embed)
        else:
            await channel.send(embed=embed)  # type: ignore


def setup(bot) -> None:
    bot.add_cog(Calendar(bot))
