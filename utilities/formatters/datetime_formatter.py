import datetime
import pytz


def format_datetime_into_isoformat(date_time: datetime.datetime) -> str:
    return date_time.replace(tzinfo=pytz.timezone("Europe/Paris")).isoformat().replace("+00:00", "Z")
