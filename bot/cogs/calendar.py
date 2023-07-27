import discord
from discord.ext import commands

from bot.bot import PRDBot
from bot.embeds.calendar import CalendarEmbed
from bot.views.calendar import CalendarPaginator
from bot.requests.event import get_events


class Calendar(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot

    @commands.slash_command(name="calendar", description="Get the calendar")
    async def calendar(self, ctx: discord.ApplicationContext):
        """Get the calendar"""
        await ctx.respond("Getting calendar...")
        events = await get_events(self.bot.http_client)
        if len(events) < 10:
            embed = await CalendarEmbed(events=events).build()
            await ctx.channel.send(embed=embed)
        else:
            paginator = await CalendarPaginator(events=events).build()
            await paginator.send_message(channel=ctx.channel)


def setup(bot) -> None:
    bot.add_cog(Calendar(bot))
