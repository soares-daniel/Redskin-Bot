from typing import List

import discord

from bot.embeds.calendar import CalendarEmbed
from models.schemas.event import EventInResponse


class CalendarPaginator(discord.ui.View):
    def __init__(self, events: List[EventInResponse], *args, **kwargs) -> None:
        super().__init__(timeout=None, *args, **kwargs)
        self.custom_id = "calendar_paginator"
        self.events = events
        self.current_page = 0
        self.last_page = 0
        self.indexed_events = dict()  # separate events in months
        self._pages = list()
        self.current_embed = None

    async def send_message(self, channel: discord.TextChannel) -> None:
        """Send message"""
        self._message = await channel.send(embed=self.current_embed, view=self)

    async def edit_message(self, message: discord.Message) -> None:
        """Edit message"""
        self._message = message
        await self.update_message()

    async def update_message(self) -> None:
        """Update message"""
        embed = await self.create_embed(self.indexed_events[list(self.indexed_events.keys())[self.current_page]])
        await self._message.edit(embed=embed, view=self)

    async def update_buttons(self):
        """Update buttons"""
        if self.current_page == 0:
            self.first_month.disabled = True
            self.previous_month.disabled = True
        else:
            self.first_month.disabled = False
            self.previous_month.disabled = False
        if self.current_page == self.last_page:
            self.last_month.disabled = True
            self.next_month.disabled = True
        else:
            self.last_month.disabled = False
            self.next_month.disabled = False

    async def create_embed(self, events) -> discord.Embed:
        """Create embed for month"""
        embed = await CalendarEmbed(events=events).build()
        self.current_embed = embed
        return self.current_embed

    async def build(self) -> discord.ui.View:
        """Build paginator"""
        # Remove events which are not in the future
        self.events = [event for event in self.events if event.end_date >= discord.utils.utcnow()]

        # Get months and separate events in months
        # dict = {page: [events]}
        # month = ex. 02.2023
        months = list(dict.fromkeys([event.start_date.strftime("%m.%Y") for event in self.events]))
        for month in months:
            events = list(event for event in self.events if event.start_date.strftime("%m.%Y") == month)
            self.indexed_events[month] = events
        self.last_page = len(months) - 1

        # Create embed for current month
        await self.create_embed(self.indexed_events[list(self.indexed_events.keys())[self.current_page]])

        self.first_month.disabled = True
        self.previous_month.disabled = True

        return self

    # 1. button actual month
    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple, custom_id="first_month")
    async def first_month(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.current_page = 0
        await self.update_buttons()
        await self.update_message()

    # 2. button previous month
    @discord.ui.button(label="←", style=discord.ButtonStyle.blurple, custom_id="previous_month")
    async def previous_month(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_buttons()
        await self.update_message()

    # 3. button next month
    @discord.ui.button(label="→", style=discord.ButtonStyle.blurple, custom_id="next_month")
    async def next_month(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.current_page += 1
        await self.update_buttons()
        await self.update_message()

    # 4. button last month
    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple, custom_id="last_month")
    async def last_month(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.current_page = self.last_page
        await self.update_buttons()
        await self.update_message()
