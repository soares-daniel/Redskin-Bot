import json
import logging
from logging import handlers

import discord
from aiohttp import web
from discord import Activity, ActivityType, Intents, ApplicationCommand
from discord.ext import commands

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
                      CATEGORY_NAME, CALENDAR_CHANNEL_NAME, NOTIFICATION_CHANNEL_NAME, COMMAND_CHANNEL_NAME)


class PRDBot(commands.Bot):
    """The PRD Discord bot."""

    def __init__(self) -> None:
        # Bot
        activity = Activity(type=ActivityType.watching, name="Kalendar")
        intents = Intents.all()
        super().__init__(activity=activity, command_prefix="!", intents=intents)
        
        # Logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        file_handler = handlers.TimedRotatingFileHandler(
            filename="logs/discord.log", when="midnight", backupCount=7
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(name)s - %(funcName)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        self.file_handler = file_handler
        self.stream_handler = stream_handler
        self.logger = logger

        # Backend
        self.auth_user = None
        self.http_client: HttpClient = HttpClient(self.get_token, self.set_auth_user)

        self.MAIN_GUILD = None

        # Channels
        self.CALENDAR_CHANNEL_ID = -1
        self.NOTIFICATION_CHANNEL_ID = -1
        self.COMMAND_CHANNEL_ID = -1

    async def on_ready(self) -> None:
        print("------")
        print("Les Peaux Rouges - Discord Bot")
        print(self.user.name)
        print("------")
        await self.init_channels()
        print("------")
        try:
            await login(self.get_http_client, self.set_auth_user)
        except ConnectionRefusedError as e:
            print(e)
            await self.close()
        print("------")
        await self.start_server()
        print("------")
        print("READY TO GO !")

    async def register_command(
            self, command: ApplicationCommand, force: bool = True, guild_ids: list[int] | None = None
    ) -> None:
        pass

    def get_token(self) -> str:
        if self.auth_user is None:
            return ""
        return self.auth_user.authorized_user.token

    def set_auth_user(self, auth_user) -> None:
        self.auth_user = auth_user

    def get_http_client(self):
        return lambda: self.http_client

    async def init_channels(self):
        print("INITIALIZING CHANNELS...")
        guild = self.get_guild(int(GUILD_ID))
        self.MAIN_GUILD = guild
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(CATEGORY_NAME)
            print("CATEGORY CREATED")

        calendar_channel = discord.utils.get(guild.channels, name=CALENDAR_CHANNEL_NAME.lower())
        if calendar_channel is None:
            calendar_channel = await guild.create_text_channel(CALENDAR_CHANNEL_NAME, category=category)
            print("CALENDAR CHANNEL CREATED")

        notification_channel = discord.utils.get(guild.channels, name=NOTIFICATION_CHANNEL_NAME.lower())
        if notification_channel is None:
            notification_channel = await guild.create_text_channel(NOTIFICATION_CHANNEL_NAME, category=category)
            print("NOTIFICATION CHANNEL CREATED")

        command_channel = discord.utils.get(guild.channels, name=COMMAND_CHANNEL_NAME.lower())
        if command_channel is None:
            command_channel = await guild.create_text_channel(COMMAND_CHANNEL_NAME, category=category)
            print("COMMAND CHANNEL CREATED")

        self.CALENDAR_CHANNEL_ID = calendar_channel.id
        self.NOTIFICATION_CHANNEL_ID = notification_channel.id
        self.COMMAND_CHANNEL_ID = command_channel.id
        print("CHANNELS INITIALIZED")

    async def start_server(self):
        print("STARTING SERVER...")
        app = web.Application()
        app.router.add_post(NOTIFICATION_ENDPOINT, self.on_event)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner=runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        print(f"SERVER STARTED. AWAITING EVENTS ON: {NOTIFICATION_ENDPOINT}")

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

        else:
            print(f"Unsupported operation type: {operation_type}")

            return web.Response()

    async def create_calendar(self):
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
