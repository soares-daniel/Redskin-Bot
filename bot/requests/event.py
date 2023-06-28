from bot.requests.http_client import HttpClient
from models.schemas.event_type import EventTypeInResponse
from settings import API_URL
from models.schemas.event import EventInResponse

EVENT_URL = f"{API_URL}/events"


async def get_events(
        http_client: HttpClient
) -> list[EventInResponse]:
    """Get all events"""
    db_events = await http_client.get(EVENT_URL)
    db_event_list = list()
    for db_event in db_events:  # type: ignore
        event = EventInResponse(
            id=db_event.get("id"),
            event=db_event.get("event"),
            created_at=db_event.get("created_at"),
            updated_at=db_event.get("updated_at"),
        )
        db_event_list.append(event)

    return db_event_list


async def get_event_types(
        http_client: HttpClient
) -> list[EventTypeInResponse]:
    """Get all event types"""
    db_event_types = await http_client.get(f"{EVENT_URL}/event_types")
    db_event_type_list = list()
    for db_event_type in db_event_types:  # type: ignore
        event_type = EventTypeInResponse(
            id=db_event_type.get("id"),
            name=db_event_type.get("name"),
            description=db_event_type.get("description"),
        )
        db_event_type_list.append(event_type)

    return db_event_type_list
