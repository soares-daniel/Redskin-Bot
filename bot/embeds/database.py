import discord

from bot.requests.user import get_users, get_user_roles
from bot.requests.role import get_roles, get_role_event_types
from bot.requests.event import get_event_types


class UserEmbed(discord.Embed):
    """User embed"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = "User Table"
        self.color = discord.Colour.green()

    async def load_users(self):
        users = await get_users()
        ids = [str(user.id) for user in users]
        usernames = [user.authorized_user.username for user in users]
        self.add_field(name="ID", value="\n".join(ids), inline=True)
        self.add_field(name="Username", value="\n".join(usernames), inline=True)

        roles_list = []
        for user in users:
            roles = await get_user_roles(user.id)
            role_ids = [str(role.id) for role in roles]
            roles_list.append(' - '.join(role_ids))

        self.add_field(name="Roles", value="\n".join(roles_list), inline=True)


class RoleEmbed(discord.Embed):
    """Role embed"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = "Role Table"
        self.color = discord.Colour.red()

    async def load_roles(self):
        roles = await get_roles()
        ids = [str(role.id) for role in roles]
        names = [role.name for role in roles]
        self.add_field(name="ID", value="\n".join(ids), inline=True)
        self.add_field(name="Name", value="\n".join(names), inline=True)


class EventTypeEmbed(discord.Embed):
    """EventType embed"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = "EventType Table"
        self.color = discord.Colour.blue()

    async def load_event_types(self):
        event_types = await get_event_types()
        ids = [str(event_type.id) for event_type in event_types]
        names = [event_type.name for event_type in event_types]
        descriptions = [event_type.description for event_type in event_types]
        self.add_field(name="ID", value="\n".join(ids), inline=True)
        self.add_field(name="Name", value="\n".join(names), inline=True)
        self.add_field(name="Description", value="\n".join(descriptions), inline=True)


class RoleEventTypeEmbed(discord.Embed):
    """RoleEventType embed"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = "RoleEventType Table"
        self.color = discord.Colour.purple()

    async def load_role_event_types(self):
        role_event_types = await get_role_event_types()
        event_type_ids = [str(role_event_type.event_type_id) for role_event_type in role_event_types]
        role_ids = [str(role_event_type.role_id) for role_event_type in role_event_types]
        self.add_field(name="EventType ID", value="\n".join(event_type_ids), inline=True)
        self.add_field(name="Role ID", value="\n".join(role_ids), inline=True)
        # Permissions field
        results = []
        for role_event_type in role_event_types:
            permissions = [role_event_type.can_edit, role_event_type.can_see, role_event_type.can_add]
            result = ""
            for permission in permissions:
                result += "✅" if permission else "❌"
                result += "\n"
            results.append(result)
        self.add_field(name="See/Add/Edit", value="\n".join(results), inline=True)
