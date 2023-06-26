import logging

from discord.ext import commands

from bot.embeds.database import UserEmbed, RoleEmbed, EventTypeEmbed, RoleEventTypeEmbed


class Database(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.bot.file_handler)
        self.logger.addHandler(self.bot.stream_handler)

    @commands.slash_command(name="database", description="Get tables from the database")
    async def database_info(self, ctx):
        """Get tables from the database"""
        await ctx.defer()

        user_embed = UserEmbed()
        await user_embed.load_users()
        await ctx.send(embed=user_embed)

        role_embed = RoleEmbed()
        await role_embed.load_roles()
        await ctx.send(embed=role_embed)

        event_type_embed = EventTypeEmbed()
        await event_type_embed.load_event_types()
        await ctx.send(embed=event_type_embed)

        role_event_type_embed = RoleEventTypeEmbed()
        await role_event_type_embed.load_role_event_types()
        await ctx.send(embed=role_event_type_embed)


def setup(bot) -> None:
    bot.add_cog(Database(bot))
