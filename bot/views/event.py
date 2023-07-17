from typing import List
import logging

import discord

from bot.bot import PRDBot
from bot.requests.event import get_event_types
from bot.modals.event import EventModal
from models.schemas.event_type import EventTypeInResponse


class EventSelect(discord.ui.View):
    """Event select menu"""

    def __init__(self, bot: PRDBot, logger: logging.Logger) -> None:
        super().__init__(timeout=None)
        self.bot = bot
        self.logger = logger
        self.options = [
            discord.SelectOption(
                label="Loading...",
                value="0",
                description="Loading event types...")
        ]

    async def add_options(self) -> List[discord.SelectOption]:
        """Get event types from the API and
        add them as options to the select menu"""
        event_types = await get_event_types(self.bot.http_client)
        options = list()
        for event_type in event_types:
            option = discord.SelectOption(
                label=event_type.name,
                value=str(event_type.id),
                description=event_type.description,
            )
            options.append(option)
            self.logger.debug(f"Added option {option.__str__()}")
        return options

    async def build(self):
        """Build the select menu"""
        self.options = await self.add_options()

    @discord.ui.select(
        placeholder="Select an event type",
        min_values=1,
        max_values=1,
        custom_id="event_select",
    )
    async def select_callback(
            self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        """Callback for the select menu"""
        value = int(select.values[0])
        event_type: EventTypeInResponse = EventTypeInResponse()
        event_type.id = value
        event_type.name = select.options[value].label
        event_type.description = select.options[value].description

        await interaction.message.edit(view=self)
        await interaction.response.send_modal(
            EventModal(self.bot, self.logger, event_type)
        )
        self.logger.info(f"User {interaction.user.name} selected event type {value}")
