from datetime import datetime, timedelta

from src.common.datetime_utils import distance_of_time_in_words


def test_time_distance_in_words() -> None:
    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0)
    assert distance_of_time_in_words(t1, t2) == "less than a minute"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=1)
    assert distance_of_time_in_words(t1, t2) == "1 minute"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=44)
    assert distance_of_time_in_words(t1, t2) == "44 minutes"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=45)
    assert distance_of_time_in_words(t1, t2) == "about 1 hour"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=89)
    assert distance_of_time_in_words(t1, t2) == "about 1 hour"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=90)
    assert distance_of_time_in_words(t1, t2) == "about 2 hours"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=1333)
    assert distance_of_time_in_words(t1, t2) == "about 22 hours"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=1439)
    assert distance_of_time_in_words(t1, t2) == "about 24 hours"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=1440)
    assert distance_of_time_in_words(t1, t2) == "1 day"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=2519)
    assert distance_of_time_in_words(t1, t2) == "1 day"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=2520)
    assert distance_of_time_in_words(t1, t2) == "2 days"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=33000)
    assert distance_of_time_in_words(t1, t2) == "23 days"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=43199)
    assert distance_of_time_in_words(t1, t2) == "30 days"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=43200)
    assert distance_of_time_in_words(t1, t2) == "about 1 month"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=86399)
    assert distance_of_time_in_words(t1, t2) == "about 2 months"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=86400)
    assert distance_of_time_in_words(t1, t2) == "2 months"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=525599)
    assert distance_of_time_in_words(t1, t2) == "12 months"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=525600)
    assert distance_of_time_in_words(t1, t2) == "almost 1 year"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=925600)
    assert distance_of_time_in_words(t1, t2) == "almost 2 years"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=5025600)
    assert distance_of_time_in_words(t1, t2) == "over 9 years"

    t1 = datetime(2024, 1, 1, 0, 0, 0)
    t2 = datetime(2024, 1, 1, 0, 0, 0) + timedelta(minutes=4225600)
    assert distance_of_time_in_words(t1, t2) == "about 8 years"

