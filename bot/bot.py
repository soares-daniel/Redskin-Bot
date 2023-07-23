import sys
import json

import discord
from discord import Activity, ActivityType, Intents, ApplicationCommand
from discord.ext import commands
from aiohttp import web
from loguru import logger

from bot.embeds.calendar import CalendarEmbed
from bot.embeds.logging import (LogEmbed, EventLog, EventTypeLog, RoleLog,
                                UserLog, UserRoleLog, PermissionLog)
from models.schemas.event import EventInResponse
from models.schemas.event_type import EventTypeInResponse
from models.schemas.role import RoleInResponse
from models.schemas.user import UserInResponse
from models.schemas.user_role import UserRoleInAssign
from models.schemas.role_event_type import RoleEventTypeInResponse


from bot.requests.http_client import HttpClient
from bot.requests.event import get_events
from bot.authorization.backend import login
from settings import (SERVER_PORT, SERVER_HOST, NOTIFICATION_ENDPOINT, GUILD_ID,
                      CATEGORY_NAME, CALENDAR_CHANNEL_NAME, NOTIFICATION_CHANNEL_NAME,
                      COMMAND_CHANNEL_NAME, EVENT_CHANNEL_NAME)


class PRDBot(commands.Bot):
    """The PRD Discord bot"""

    def __init__(self) -> None:
        # Bot
        activity = Activity(type=ActivityType.watching, name="Kalendar")
        intents = Intents.all()
        super().__init__(activity=activity, command_prefix="!", intents=intents)
        
        # logger
        LOGGING_FORMAT = "<green>{time:HH:mm:ss.SSSZ}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        logger.remove()
        logger.add("logs/discord.log", rotation="00:00", format=LOGGING_FORMAT, level="DEBUG", retention="7 days")
        logger.add(sys.stdout, colorize=True, format=LOGGING_FORMAT, level="INFO")

        self.logger = logger

        # Backend
        self.auth_user = None
        self.http_client: HttpClient = HttpClient(
            set_auth_user=self.set_auth_user,
            logger=self.logger
        )
        self.notification_server = None

        self.MAIN_GUILD = None
        self.CATEGORY = None

        # Channels
        self.CALENDAR_CHANNEL_ID = -1
        self.NOTIFICATION_CHANNEL_ID = -1
        self.COMMAND_CHANNEL_ID = -1
        self.EVENT_CHANNEL_ID = -1

    async def on_ready(self) -> None:
        """Set up the bot when it's ready"""
        self.logger.info("------")
        self.logger.info("Les Peaux Rouges - Discord Bot")
        self.logger.info(self.user.name)
        self.logger.info("------")
        await self.init_channels()
        self.logger.info("------")
        try:
            await login(self.get_http_client, self.set_auth_user, self.logger)
        except ConnectionRefusedError as e:
            self.logger.exception(e)
            await self.close()
        self.logger.info("------")
        await self.start_server()
        self.logger.info("------")
        self.logger.info("Bot ready")

    async def register_command(
            self, command: ApplicationCommand, force: bool = True, guild_ids: list[int] | None = None
    ) -> None:
        pass

    def set_auth_user(self, auth_user) -> None:
        """Set the authorized user"""
        self.auth_user = auth_user

    def get_http_client(self):
        """Get the http client"""
        return lambda: self.http_client

    async def init_channels(self):
        """Initialize the channels if they don't exist"""
        self.logger.info("Initializing channels...")
        guild = self.get_guild(int(GUILD_ID))
        self.MAIN_GUILD = guild
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        self.CATEGORY = category
        if category is None:
            category = await guild.create_category(CATEGORY_NAME)
            self.logger.debug("Category created")

        calendar_channel = discord.utils.get(guild.channels, name=CALENDAR_CHANNEL_NAME.lower())
        if calendar_channel is None:
            calendar_channel = await guild.create_text_channel(CALENDAR_CHANNEL_NAME, category=category)
            self.logger.debug("Calendar channel created")

        notification_channel = discord.utils.get(guild.channels, name=NOTIFICATION_CHANNEL_NAME.lower())
        if notification_channel is None:
            notification_channel = await guild.create_text_channel(NOTIFICATION_CHANNEL_NAME, category=category)
            self.logger.debug("Notification channel created")

        command_channel = discord.utils.get(guild.channels, name=COMMAND_CHANNEL_NAME.lower())
        if command_channel is None:
            command_channel = await guild.create_text_channel(COMMAND_CHANNEL_NAME, category=category)
            self.logger.debug("Command channel created")

        event_channel = discord.utils.get(guild.channels, name=EVENT_CHANNEL_NAME.lower())
        if event_channel is None:
            event_channel = await guild.create_text_channel(EVENT_CHANNEL_NAME, category=category)
            self.logger.debug("Event channel created")

        self.CALENDAR_CHANNEL_ID = calendar_channel.id
        self.NOTIFICATION_CHANNEL_ID = notification_channel.id
        self.COMMAND_CHANNEL_ID = command_channel.id
        self.EVENT_CHANNEL_ID = event_channel.id

        self.logger.info("Channels initialized")

    async def start_server(self):
        """Start the server to receive events from the backend"""
        self.logger.info("Starting server...")
        app = web.Application()
        app.router.add_post(NOTIFICATION_ENDPOINT, self.on_event)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner=runner, host=SERVER_HOST, port=SERVER_PORT)
        self.logger.info(f"Server will listen on: {SERVER_HOST}:{SERVER_PORT}")
        await site.start()
        self.notification_server = site
        self.logger.info(f"Server started. Awaiting events on: {NOTIFICATION_ENDPOINT}")

    async def on_event(self, request):
        response = await request.json()
        event_operation = response['event_operation']

        # Define a mapping from operation types to data models
        model_map = {
            "event": EventInResponse,
            "event_type": EventTypeInResponse,
            "role": RoleInResponse,
            "user": UserInResponse,
            "user_role": UserRoleInAssign,  # Remove and assign are the same model
            "permission": RoleEventTypeInResponse
        }

        # Extract the type of operation (e.g., 'event', 'user', etc.) from the operation string
        operation_type = event_operation.split('_')[0]

        # Use the map to get the appropriate model class
        ModelClass = model_map.get(operation_type)

        if ModelClass is not None:
            # Deserialize the JSON data into a model object
            event = ModelClass.parse_obj(json.loads(response['event']))

            # Define a mapping from operation types to LogEmbed subclasses
            log_class_map = {
                "event": EventLog,
                "event_type": EventTypeLog,
                "role": RoleLog,
                "user": UserLog,
                "user_role": UserRoleLog,
                "permission": PermissionLog
            }

            # Use the map to get the appropriate log class, and fall back to LogEmbed class if type not recognized
            LogClass = log_class_map.get(operation_type, LogEmbed)

            # Instantiate the log object and load the data
            log = LogClass()
            await log.load_data(event_operation.split('_')[1], event)

            # Send the embed
            channel = await self.fetch_channel(self.NOTIFICATION_CHANNEL_ID)
            if channel:
                await channel.send(embed=log)

            # Update calendar if event
            if operation_type == "event":
                await self.create_calendar()

            self.logger.debug(f"Received event: {response}")
            return web.Response(text="OK")
        else:
            self.logger.error(f"Unsupported operation type: {operation_type}")
            return web.Response()

    async def create_calendar(self):
        """Create the calendar embed"""
        self.logger.debug("Creating calendar...")
        events = await get_events(self.http_client)
        embed = await CalendarEmbed(events=events).build()
        channel = await self.fetch_channel(self.CALENDAR_CHANNEL_ID)
        if channel is None:
            return

        # Get the last message
        last_message = await channel.history(limit=1).flatten()
        if last_message:
            await last_message[0].edit(embed=embed)
        else:
            await channel.send(embed=embed)  # type: ignore

        self.logger.debug("Calendar created")
