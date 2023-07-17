import logging
import datetime

import discord

from bot.bot import PRDBot
from bot.requests.event import create_event
from models.schemas.event_type import EventTypeInResponse
from models.schemas.event import EventInCreate


class EventModal(discord.ui.Modal):
    """Event modal."""

    def __init__(self, bot: PRDBot, logger: logging.Logger, event_type: EventTypeInResponse) -> None:
        super().__init__(title=f"New Event: {event_type.name}")
        self.bot = bot
        self.logger = logger
        self.event_type = event_type
        self.add_item(
            discord.ui.InputText(
                label="Title",
                placeholder="Enter title",
                required=True,
                custom_id="title"
            ))
        self.add_item(
            discord.ui.InputText(
                label="Description",
                placeholder="Enter description",
                required=True,
                style=discord.InputTextStyle.long,
                custom_id="description"
            ))
        self.add_item(
            discord.ui.InputText(
                label="Start Date (DD/MM/YYYY - HH:MM)",
                placeholder="DD/MM/YYYY - HH:MM",
                required=True,
                custom_id="start_date",
            ))
        self.add_item(
            discord.ui.InputText(
                label="End Date (DD/MM/YYYY - HH:MM)",
                placeholder="DD/MM/YYYY - HH:MM",
                required=True,
                custom_id="end_date",
            ))

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for the modal."""
        # Parse fields and validate
        title = self.children[0].value
        description = self.children[1].value
        start_date_str = self.children[2].value
        end_date_str = self.children[3].value
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y - %H:%M")
            end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y - %H:%M")
        except ValueError:
            await interaction.followup.send(
                "Invalid date format. Please try again.",
                ephemeral=True,
                delete_after=5
            )
            return

        # Create event
        event = EventInCreate()
        event.created_by = 2  # Superuser
        event.event_type = self.event_type.id
        event.title = title
        event.description = description
        event.start_date = start_date
        event.end_date = end_date
        created_event = await create_event(self.bot.http_client, event)

        if created_event:
            await interaction.followup.send(
                "Event created! The calendar will be updated shortly.",
                ephemeral=True,
                delete_after=5
            )
        else:
            await interaction.followup.send(
                "An error occurred. Please try again.",
                ephemeral=True,
                delete_after=5
            )
