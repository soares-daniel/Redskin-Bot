import discord
from discord.ext import commands

from bot.bot import PRDBot


class Admin(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot

    async def close_connections(self) -> None:
        # HTTP Client
        await self.bot.http_client.close()

        # Notification server
        await self.bot.notification_server.close()

    @commands.slash_command(name="shutdown", description="For safely shutting down the bot")
    async def shutdown(self, ctx: discord.ApplicationContext):
        await ctx.send("Shutting down...")
        await self.close_connections()
        await self.bot.close()


def setup(bot) -> None:
    bot.add_cog(Admin(bot))
