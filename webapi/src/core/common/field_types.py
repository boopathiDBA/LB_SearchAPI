from datetime import datetime
from typing import Annotated

import pytz
from pydantic import PlainSerializer

LOCAL_TIMEZONE = pytz.timezone("Australia/Sydney")


def _convert_datetime_to_local_datetime(dt: datetime) -> datetime:
    """
    If the datetime is already in local timezone, it will be returned as is.

    If the datetime is in another timezone, it will be converted to local timezone.

    If the datetime has no timezone information, it will be assumed to be in UTC timezone
    and converted to local timezone.
    """
    # Check if datetime has timezone information
    if dt.tzinfo is not None and hasattr(dt.tzinfo, "zone"):
        # Check if datetime is already in local timezone
        if getattr(dt.tzinfo, "zone") == LOCAL_TIMEZONE.zone:
            return dt
        # Convert from other timezone to local timezone
        else:
            return dt.astimezone(LOCAL_TIMEZONE)
    else:
        # Assume datetime is UTC time and return local time
        return dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIMEZONE)


"""
This type represents an input of datetime that is in UTC timezone and will be converted to local timezone.

We have this type as opposed to using `datetime` directly to make it clear that the input is expected to be in UTC timezone
and will be serialized to local timezone on data export/dump.

Currently we assume that all data in the database is store in UTC timezone and we don't want to do any conversion in 
SQL queries so this typing will handle when we serialized when dumping entity data.

NOTE: Any fields that this is assigned to will still be of type datetime without any timezone information.
Only when dumping data will the value be serialized to local timezone.
"""
UtcDatetime = Annotated[
    datetime, PlainSerializer(_convert_datetime_to_local_datetime, return_type=datetime)
]
