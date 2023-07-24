from typing import List
import logging

import discord

from bot.requests.event import get_event_types
from bot.modals.event import EventModal
from models.schemas.event_type import EventTypeInResponse


class EventSelect(discord.ui.Select):
    """Event select menu"""

    def __init__(self, bot, logger: logging.Logger) -> None:
        self.bot = bot
        self.logger = logger
        super().__init__(
            placeholder="Create a new event",
            min_values=1,
            max_values=1,
            options=self.add_options(),
            custom_id="event_select",
        )

    def add_options(self) -> List[discord.SelectOption]:
        """Get event types from the API and
        add them as options to the select menu"""
        event_types = get_event_types(self.bot.http_client)
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

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for the select menu"""
        value = int(self.values[0])
        event_type: EventTypeInResponse = EventTypeInResponse(
            id=value,
            name=self.options[value-1].label,
            description=self.options[value-1].description,
        )
        await interaction.response.send_modal(
            EventModal(self.bot, self.logger, event_type)
        )
        self.logger.info(f"User {interaction.user.name} selected event type {value}")


class EventView(discord.ui.View):
    def __init__(self, bot, logger: logging.Logger) -> None:
        self.bot = bot
        self.logger = logger
        super().__init__(timeout=None)
        self.add_item(EventSelect(self.bot, self.logger))
