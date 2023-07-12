from typing import List

import discord

from models.schemas.event import EventInResponse


async def get_days_from_events(events: List[EventInResponse]) -> List[str]:
    """Get days from events"""
    days = list()
    for event in events:
        days.append(event.start_date.strftime("%d.%m.%Y"))

    return days


async def get_events_for_day(events: List[EventInResponse], day: str) -> List[EventInResponse]:
    """Get events for day"""
    events_for_day = list()
    for event in events:
        if event.start_date.strftime("%d.%m.%Y") == day:
            events_for_day.append(event)

    return events_for_day


# TODO: Change to Paginator, when too many events
class CalendarEmbed(discord.Embed):
    def __init__(self, events: List[EventInResponse], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.events = events
        self.title = "CALENDAR"
        self.set_footer(text=f"Last updated · {str(discord.utils.utcnow())}  · Timezone: UTC")

    async def build(self) -> discord.Embed:
        """Build embed"""
        self.clear_fields()
        days = await get_days_from_events(self.events)
        for day in days:
            events_for_day = await get_events_for_day(self.events, day)
            events = ""
            for event in events_for_day:
                day = f"**{event.start_date.strftime('%A')}** - {day}"
                # Format event like this: 10:00 - 14:30 | Eventname in code block
                event = f"{event.start_date.strftime('%H:%M')} - {event.end_date.strftime('%H:%M')} | {event.title}"

            block = f"```{events}```"
            self.add_field(name=day, value=block, inline=False)

        return self
