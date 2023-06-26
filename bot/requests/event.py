import aiohttp

from models.schemas.event_type import EventTypeInResponse
from settings import API_URL
from models.schemas.event import EventInResponse

EVENT_URL = f"{API_URL}/events"


async def get_events() -> list[EventInResponse]:
    """Get all events"""
    async with aiohttp.ClientSession() as session:
        async with session.get(EVENT_URL) as response:
            db_events = await response.json()
            db_event_list = list()
            for db_event in db_events:
                event = EventInResponse(
                    id=db_event.get("id"),
                    event=db_event.get("event"),
                    created_at=db_event.get("created_at"),
                    updated_at=db_event.get("updated_at"),
                )
                db_event_list.append(event)

    return db_event_list


# TODO: FIX 401 UNAUTHORIZED (create session_token with autorenewal)
async def get_event_types() -> list[EventTypeInResponse]:
    """Get all event types"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{EVENT_URL}/event_types") as response:
            db_event_types = await response.json()
            db_event_type_list = list()
            for db_event_type in db_event_types:
                event_type = EventTypeInResponse(
                    name=db_event_type.get("name"),
                    description=db_event_type.get("description"),
                )
                db_event_type_list.append(event_type)

    return db_event_type_list
