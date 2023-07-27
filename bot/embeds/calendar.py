import datetime
from typing import List

import discord

from models.schemas.event import EventInResponse


def format_date(date: datetime.datetime) -> str:
    """Format date"""
    return date.strftime("%A - %d.%m.%Y")


async def get_days_from_events(events: List[EventInResponse]) -> List[str]:
    """Get days from events"""
    days = list()
    for event in events:
        days.append(format_date(event.start_date))

    # Remove duplicates
    days = list(dict.fromkeys(days))

    # Sort
    days.sort(key=lambda x: datetime.datetime.strptime(x, "%A - %d.%m.%Y"))

    return days


async def get_events_for_day(events: List[EventInResponse], day: str) -> List[EventInResponse]:
    """Get events for day"""
    events_for_day = list()
    for event in events:
        if format_date(event.start_date) == day:
            events_for_day.append(event)

    return events_for_day


async def get_symbol_for_event_type(event_type: int) -> str:
    """Get symbol for event type"""
    if event_type == 1:  # scout_event
        return "🔴"
    elif event_type == 2:  # committee_event
        return "🟡"
    elif event_type == 3:  # chalet
        return "🔵"
    else:
        return "⚪"


# TODO: Change to Paginator, when too many events
# TODO: CHANGE TIMEZONE (IN API TOO)
class CalendarEmbed(discord.Embed):
    def __init__(self, events: List[EventInResponse], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.events = events
        calendar_logo = "https://cdn-icons-png.flaticon.com/512/4206/4206324.png"
        self.set_thumbnail(url=calendar_logo)
        self.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        self.title = f"CALENDAR"
        self.set_footer(text=f"Last updated : {discord.utils.utcnow().strftime('%d/%m/%Y %H:%M:%S UTC')}")

    async def build(self) -> discord.Embed:
        """Build embed"""
        self.clear_fields()
        if not self.events:
            url = "https://www.youtube.com/watch?v=ewf-8rx9_uQ&ab_channel=HideakiUtsumi"
            self.description = f"**No upcoming events. Check back [later]({url})!**"
            return self

        days = await get_days_from_events(self.events)
        for day in days:
            events_for_day = await get_events_for_day(self.events, day)
            events = ""
            for event in events_for_day:
                # Event Format: ⚪ | 10:00 - 14:30 | Event name in code block
                symbol = await get_symbol_for_event_type(event.event_type)
                events += f"{symbol} | {event.start_date.strftime('%H:%M')} - {event.end_date.strftime('%H:%M')} | {event.title}\n"

            block = f"```{events}```"
            self.add_field(name=day, value=block, inline=False)

        return self
