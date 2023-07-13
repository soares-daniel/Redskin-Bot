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

    @commands.slash_command(name="test_user", description="Creates and deletes a user for testing purposes")
    async def test_user(self, ctx: discord.ApplicationContext):
        await ctx.respond("Creating user...")

        url = f"{API_URL}/users/create"
        user = {
            "username": "test_user",
            "password": "test_password"
            }

        new_user = await self.bot.http_client.post(url=url, data=user)
        await ctx.send(f"Created user:\n{new_user}")

        await ctx.send("Deleting user...")

        user_id = new_user.get('id')  # type: ignore
        url = f"{API_URL}/users/delete/{user_id}"
        await self.bot.http_client.delete(url=url)
        await ctx.send(f"Deleted user: {user_id}")

    @commands.slash_command(name="test_5_events", description="Creates 5 events for testing purposes")
    async def test_5_events(self, ctx: discord.ApplicationContext):
        await ctx.respond("Creating 5 events...")

        events = [
            {
                "createdBy": 2,
                "eventType": 1,
                "title": "Outdoor Adventure Race",
                "description": "A full day of fun and friendly competition, exploring nature and learning navigation skills.",
                "startDate": "2023-07-15T09:00:00",
                "endDate": "2023-07-16T18:00:00"
            },
            {
                "createdBy": 2,
                "eventType": 2,
                "title": "Community Service Day",
                "description": "Helping our community by participating in a local cleanup project. Let's make a positive impact together!",
                "startDate": "2023-07-22T09:00:00",
                "endDate": "2023-07-23T18:00:00"
            },
            {
                "createdBy": 2,
                "eventType": 3,
                "title": "Chalet",
                "description": "A weekend of fun and relaxation at the chalet.",
                "startDate": "2023-07-29T09:00:00",
                "endDate": "2023-07-30T18:00:00"
            },
            {
                "createdBy": 2,
                "eventType": 1,
                "title": "Scout Skills Boot Camp",
                "description": "A day to learn and practice essential scouting skills such as knot tying, orienteering, and first aid.",
                "startDate": "2023-08-05T09:00:00",
                "endDate": "2023-08-06T18:00:00"
            },
            {
                "createdBy": 2,
                "eventType": 2,
                "title": "Campfire Storytelling Night",
                "description": "A night to share stories, experiences, and lessons learned around the campfire. Don't forget your marshmallows!",
                "startDate": "2023-08-12T19:00:00",
                "endDate": "2023-08-13T10:00:00"
            }
        ]

        for event in events:
            url = f"{API_URL}/events/create"
            await self.bot.http_client.post(url=url, data=event)
            await ctx.send(f"Created event '{event['title']}'")

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
