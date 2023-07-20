import discord
from discord.ext import commands

from bot.bot import PRDBot
from bot.embeds.database import UserEmbed, RoleEmbed, EventTypeEmbed, RoleEventTypeEmbed


class Database(commands.Cog):
    def __init__(self, bot: PRDBot) -> None:
        self.bot = bot

    @commands.slash_command(name="database", description="Get tables from the database")
    async def database_info(self, ctx: discord.ApplicationContext):
        """Get tables from the database"""
        await ctx.respond("Getting database info...")

        user_embed = UserEmbed(self.bot)
        await user_embed.load_users()
        await ctx.send(embed=user_embed)

        role_embed = RoleEmbed(self.bot)
        await role_embed.load_roles()
        await ctx.send(embed=role_embed)

        event_type_embed = EventTypeEmbed(self.bot)
        await event_type_embed.load_event_types()
        await ctx.send(embed=event_type_embed)

        role_event_type_embed = RoleEventTypeEmbed(self.bot)
        await role_event_type_embed.load_role_event_types()
        await ctx.send(embed=role_event_type_embed)


def setup(bot) -> None:
    bot.add_cog(Database(bot))
