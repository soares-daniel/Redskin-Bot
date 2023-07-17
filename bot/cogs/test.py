import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from bot.bot import PRDBot
from bot.requests.event import get_events
from settings import API_URL


class Test(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.bot.file_handler)
        self.logger.addHandler(self.bot.stream_handler)

    @commands.slash_command(name="test_event", description="Creates and deletes an event for testing purposes")
    async def test_event(self, ctx: discord.ApplicationContext):
        await ctx.respond("Creating event...")

        today = datetime.today()
        tomorrow = today + timedelta(days=1)

        url = f"{API_URL}/events/create"
        event = {
          "createdBy": 2,
          "eventType": 1,
          "title": "test event",
          "description": "for testing purposes",
          "startDate": today.isoformat(),
          "endDate": tomorrow.isoformat()
        }

        new_event = await self.bot.http_client.post(url=url, data=event)
        await ctx.send(f"Created event:\n{new_event}")

        await ctx.send("Deleting event...")

        event_id = new_event.get('id')  # type: ignore
        url = f"{API_URL}/events/delete/{event_id}"
        await self.bot.http_client.delete(url=url)
        await ctx.send(f"Deleted event: {event_id}")

    @commands.slash_command(name="del_all_events", description="Deletes all events for testing purposes")
    async def del_all_events(self, ctx: discord.ApplicationContext):
        await ctx.respond("Deleting all events...")

        url = f"{API_URL}/events"
        events = await get_events(self.bot.http_client)
        for event in events:
            event_id = event.id  # type: ignore
            url = f"{API_URL}/events/delete/{event_id}"
            await self.bot.http_client.delete(url=url)
            await ctx.send(f"Deleted event {event_id}")


def setup(bot) -> None:
    bot.add_cog(Test(bot))
