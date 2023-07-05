import discord

from bot.bot import PRDBot
from bot.requests.user import get_users, get_user_roles
from bot.requests.role import get_roles, get_role_event_types
from bot.requests.event import get_event_types


class DatabaseEmbed(discord.Embed):
    def __init__(self, bot: PRDBot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.http_client = bot.http_client

    async def load_items(self, getter, *field_funcs):
        items = await getter(self.http_client)
        for field_name, field_func in field_funcs:
            values = [field_func(item) for item in items]
            self.add_field(name=field_name.capitalize(), value="\n".join(map(str, values)), inline=True)


class UserEmbed(DatabaseEmbed):
    """User embed"""
    def __init__(self, bot: PRDBot, *args, **kwargs) -> None:
        super().__init__(bot=bot, *args, **kwargs)
        self.title = "User Table"
        self.color = discord.Colour.green()

    async def load_users(self):
        await self.load_items(
            get_users,
            ("id", lambda user: user.id),
            ("username", lambda user: user.authorized_user.username)
        )


class RoleEmbed(DatabaseEmbed):
    """Role embed"""
    def __init__(self, bot: PRDBot, *args, **kwargs) -> None:
        super().__init__(bot=bot, *args, **kwargs)
        self.title = "Role Table"
        self.color = discord.Colour.red()

    async def load_roles(self):
        await self.load_items(
            get_roles,
            ("id", lambda role: role.id),
            ("name", lambda role: role.name)
        )


class EventTypeEmbed(DatabaseEmbed):
    """EventType embed"""
    def __init__(self, bot: PRDBot, *args, **kwargs) -> None:
        super().__init__(bot=bot, *args, **kwargs)
        self.title = "EventType Table"
        self.color = discord.Colour.blue()

    async def load_event_types(self):
        await self.load_items(
            get_event_types,
            ("id", lambda event_type: event_type.id),
            ("name", lambda event_type: event_type.name),
            ("description", lambda event_type: event_type.description)
        )


class RoleEventTypeEmbed(DatabaseEmbed):
    """RoleEventType embed"""
    def __init__(self, bot: PRDBot, *args, **kwargs) -> None:
        super().__init__(bot=bot, *args, **kwargs)
        self.title = "RoleEventType Table"
        self.color = discord.Colour.purple()

    async def load_role_event_types(self):
        await self.load_items(
            get_role_event_types,
            ("EventType ID", lambda role_event_type: role_event_type.event_type_id),
            ("Role ID", lambda role_event_type: role_event_type.role_id),
            ("See/Add/Edit", lambda role_event_type: "".join(
                "✅" if perm else "❌" for perm in
                [role_event_type.can_see, role_event_type.can_add, role_event_type.can_edit]
            ))
        )
