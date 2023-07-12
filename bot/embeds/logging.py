import discord

from models.schemas.event import EventInResponse
from models.schemas.event_type import EventTypeInResponse
from models.schemas.role import RoleInResponse
from models.schemas.role_event_type import RoleEventTypeInResponse
from models.schemas.user import UserInResponse
from models.schemas.user_role import UserRoleInAssign

user_image_url = "https://pics.freeicons.io/uploads/icons/png/4987345791543238941-512.png"
role_image_url = "https://pics.freeicons.io/uploads/icons/png/17113912771681927333-512.png"
event_image_url = "https://pics.freeicons.io/uploads/icons/png/4567109991623563293-512.png"
event_type_image_url = "https://pics.freeicons.io/uploads/icons/png/9966980361555936928-512.png"
permission_image_url = "https://pics.freeicons.io/uploads/icons/png/14474864961681877876-512.png"


class LogEmbed(discord.Embed):
    """Base embed for logs"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.timestamp = discord.utils.utcnow()
        self.set_footer(text="PRD Bot")

    async def set_color(self, color: discord.Color = discord.Color.dark_gray) -> None:
        self.color = color

    async def set_color_by_operation(self, operation: str) -> None:
        if operation == "create" or operation == "assign":
            await self.set_color(discord.Color.green())
        elif operation == "update":
            await self.set_color(discord.Color.blue())
        elif operation == "delete" or operation == "remove":
            await self.set_color(discord.Color.red())

    def load_data(self, operation: str, event: dict):
        pass


class EventLog(LogEmbed):
    """Embed for event logs"""
    async def load_data(self, event_operation: str, event: EventInResponse) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=event_image_url)
        self.title = f"{event_operation} Event".upper()
        self.add_field(name="ID", value=str(event.id))
        self.add_field(name="Created By", value=str(event.created_by))
        self.add_field(name="Event Type", value=str(event.event_type))
        self.add_field(name="Title", value=event.title)
        self.add_field(name="Description", value=event.description)
        self.add_field(name="Start Date", value=str(event.start_date), inline=False)
        self.add_field(name="End Date", value=str(event.end_date), inline=False)
        self.add_field(name="Created At", value=str(event.created_at), inline=False)
        updated_at = event.updated_at
        self.add_field(name="Updated At", value=str(updated_at) if updated_at else "Never", inline=False)


class EventTypeLog(LogEmbed):
    """Embed for event type logs"""
    async def load_data(self, event_operation: str, event_type: EventTypeInResponse) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=event_type_image_url)
        self.title = f"{event_operation} Event Type".upper()
        self.add_field(name="ID", value=str(event_type.id))
        self.add_field(name="Name", value=event_type.name)
        self.add_field(name="Description", value=event_type.description, inline=False)


class RoleLog(LogEmbed):
    """Embed for role logs"""
    async def load_data(self, event_operation: str, role: RoleInResponse) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=role_image_url)
        self.title = f"{event_operation} Role".upper()
        self.add_field(name="ID", value=str(role.id))
        self.add_field(name="Name", value=role.name)


class UserLog(LogEmbed):
    """Embed for user logs"""
    async def load_data(self, event_operation: str, user: UserInResponse) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=user_image_url)
        self.title = f"{event_operation} User".upper()
        self.add_field(name="ID", value=str(user.id))
        self.add_field(name="Username", value=user.authorized_user.username)
        self.add_field(name="Created At", value=str(user.authorized_user.created_at), inline=False)
        updated_at = user.authorized_user.updated_at
        self.add_field(name="Updated At", value=str(updated_at) if updated_at else "Never", inline=False)


class UserRoleLog(LogEmbed):
    """Embed for user role logs"""
    async def load_data(self, event_operation: str, user_role: UserRoleInAssign) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=role_image_url)
        self.title = f"{event_operation} Role".upper()
        self.add_field(name="Username", value=str(user_role.username))
        self.add_field(name="Role name", value=str(user_role.role_name))


class PermissionLog(LogEmbed):
    """Embed for permission logs"""
    async def load_data(self, event_operation: str, permission: RoleEventTypeInResponse) -> None:
        await self.set_color_by_operation(event_operation)
        self.set_thumbnail(url=permission_image_url)
        self.title = f"{event_operation} Permission".upper()
        self.add_field(name="Role ID", value=str(permission.role_id))
        self.add_field(name="EventType ID", value=str(permission.event_type_id))
        self.add_field(name="", value="", inline=False)
        self.add_field(name="Can edit", value=str(permission.can_edit))
        self.add_field(name="Can see", value=str(permission.can_see))
        self.add_field(name="Can add", value=str(permission.can_add))
