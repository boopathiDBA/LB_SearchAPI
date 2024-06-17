from datetime import datetime
from enum import StrEnum


class TimeUnit(StrEnum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


MINUTES_IN_YEAR = 525600
MINUTES_IN_QUARTER_YEAR = 131400
MINUTES_IN_THREE_QUARTERS_YEAR = 394200


def _is_leap_year(year):
    """
    Determines if a year is a leap year.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _count_leap_years(start, end):
    """
    Counts the number of leap years between the start and end years, inclusive.
    """
    leap_years = [year for year in range(start, end + 1) if _is_leap_year(year)]
    return len(leap_years)


def _get_unit_text(unit: TimeUnit, amount: int):
    return unit if amount == 1 else f"{unit}s"


def distance_of_time_in_words(from_time: datetime, to_time: datetime) -> str:
    """
    This method is a port of ActionView/DateHelper method called 'distance_of_time_in_words' from ruby on rails
    source: https://github.com/rails/rails/blob/6f0d1ad14b92b9f5906e44740fce8b4f1c7075dc/actionview/lib/action_view/helpers/date_helper.rb
    """
    if from_time > to_time:
        from_time, to_time = to_time, from_time

    distance_in_minutes = round((to_time.timestamp() - from_time.timestamp()) / 60.0)

    if 0 <= distance_in_minutes <= 1:
        if distance_in_minutes == 0:
            return f"less than a minute"
        else:
            return f"{distance_in_minutes} {_get_unit_text(TimeUnit.MINUTE, distance_in_minutes)}"
    elif 2 <= distance_in_minutes < 45:
        return f"{distance_in_minutes} {_get_unit_text(TimeUnit.MINUTE, distance_in_minutes)}"
    elif 45 <= distance_in_minutes < 90:
        return f"about 1 {_get_unit_text(TimeUnit.HOUR, 1)}"
    elif 90 <= distance_in_minutes < 1440:
        hours = round(distance_in_minutes / 60)
        return f"about {hours} {_get_unit_text(TimeUnit.HOUR, hours)}"
    elif 1440 <= distance_in_minutes < 2520:
        return f"1 {_get_unit_text(TimeUnit.DAY, 1)}"
    elif 2520 <= distance_in_minutes < 43200:
        days = round(distance_in_minutes / 1440)
        return f"{days} {_get_unit_text(TimeUnit.DAY, days)}"
    elif 43200 <= distance_in_minutes < 86400:
        months = round(distance_in_minutes / 43200)
        return f"about {months} {_get_unit_text(TimeUnit.MONTH, months)}"
    elif 86400 <= distance_in_minutes < 525600:
        months = round(distance_in_minutes / 43200)
        return f"{months} {_get_unit_text(TimeUnit.MONTH, months)}"
    else:
        from_year = from_time.year
        if from_time.month >= 3:
            from_year += 1
        to_year = to_time.year
        if to_time.month < 3:
            to_year -= 1
        leap_years = 0 if from_year > to_year else _count_leap_years(from_year, to_year)
        minute_offset_for_leap_year = leap_years * 1440
        # Discount the leap year days when calculating year distance.
        # e.g. if there are 20 leap year days between 2 dates having the same day
        # and month then based on 365 days calculation
        # the distance in years will come out to over 80 years when in written
        # English it would read better as about 80 years.
        minutes_with_offset = distance_in_minutes - minute_offset_for_leap_year
        remainder = minutes_with_offset % MINUTES_IN_YEAR
        distance_in_years = int(minutes_with_offset / MINUTES_IN_YEAR)
        if remainder < MINUTES_IN_QUARTER_YEAR:
            return f"about {distance_in_years} {_get_unit_text(TimeUnit.YEAR, distance_in_years)}"
        elif remainder < MINUTES_IN_THREE_QUARTERS_YEAR:
            return f"over {distance_in_years} {_get_unit_text(TimeUnit.YEAR, distance_in_years)}"
        else:
            return f"almost {distance_in_years + 1} {_get_unit_text(TimeUnit.YEAR, distance_in_years + 1)}"
