from enum import Enum


class EventOperation(Enum):
    CREATE = "new_event"
    UPDATE = "event_updated"
    DELETE = "event_deleted"
