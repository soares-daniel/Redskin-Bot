import datetime
import pytz


def format_datetime_into_isoformat(date_time: datetime.datetime) -> str:
    return date_time.astimezone(pytz.UTC).isoformat().replace("+00:00", "Z")
