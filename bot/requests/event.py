from typing import List

import requests

from bot.requests.http_client import HttpClient
from models.schemas.event_type import EventTypeInResponse
from settings import API_URL
from models.schemas.event import EventInResponse

EVENT_URL = f"{API_URL}/events"


async def get_events(
        http_client: HttpClient
) -> List[EventInResponse]:
    """Get all events"""
    db_events = await http_client.get(f"{EVENT_URL}/user")
    db_event_list = list()
    for db_event in db_events:  # type: ignore
        event = EventInResponse(
            id=db_event.get("id"),
            created_by=db_event.get("createdBy"),
            event_type=db_event.get("eventType"),
            title=db_event.get("title"),
            description=db_event.get("description"),
            start_date=db_event.get("startDate"),
            end_date=db_event.get("endDate"),
            created_at=db_event.get("createdAt"),
            updated_at=db_event.get("updatedAt"),
        )
        db_event_list.append(event)

    return db_event_list


def get_event_types(
        http_client: HttpClient
) -> List[EventTypeInResponse]:
    """Get all event types"""

    response = requests.get(f"{EVENT_URL}/event_types")
    db_event_types = response.json()
    db_event_type_list = list()
    for db_event_type in db_event_types:  # type: ignore
        event_type = EventTypeInResponse(
            id=db_event_type.get("id"),  # type: ignore
            name=db_event_type.get("name"),  # type: ignore
            description=db_event_type.get("description"),  # type: ignore
        )
        db_event_type_list.append(event_type)

    return db_event_type_list


async def create_event(
        http_client: HttpClient,
        event: dict
) -> EventInResponse:
    """Create an event"""

    db_event = await http_client.post(url=f"{EVENT_URL}/create", data=event)  # type: ignore

    created_event = EventInResponse(
        id=db_event.get("id"),  # type: ignore
        created_by=db_event.get("createdBy"),  # type: ignore
        event_type=db_event.get("eventType"),  # type: ignore
        title=db_event.get("title"),  # type: ignore
        description=db_event.get("description"),  # type: ignore
        start_date=db_event.get("startDate"),  # type: ignore
        end_date=db_event.get("endDate"),  # type: ignore
        created_at=db_event.get("createdAt"),  # type: ignore
        updated_at=db_event.get("updatedAt"),  # type: ignore
    )

    return created_event


async def get_event_types_async(
        http_client: HttpClient
) -> List[EventTypeInResponse]:
    db_event_types = await http_client.get(f"{EVENT_URL}/event_types")
    db_event_type_list = list()
    for db_event_type in db_event_types:  # type: ignore
        event_type = EventTypeInResponse(
            id=db_event_type.get("id"),  # type: ignore
            name=db_event_type.get("name"),  # type: ignore
            description=db_event_type.get("description"),  # type: ignore
        )
        db_event_type_list.append(event_type)

    return db_event_type_list
