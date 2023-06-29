import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from bot.bot import PRDBot
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
        deleted_event = await self.bot.http_client.delete(url=url)
        await ctx.send(f"Deleted event:\n{deleted_event}")

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
        deleted_user = await self.bot.http_client.delete(url=url)
        await ctx.send(f"Deleted user:\n{deleted_user}")


def setup(bot) -> None:
    bot.add_cog(Test(bot))
