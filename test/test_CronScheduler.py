import datetime

from freezegun import freeze_time

from cron_validator.scheduler import CronScheduler


def test_round_to_nearest_minute():
    non_rounded_date = datetime.datetime(year=2020, month=8, day=15, hour=12, minute=24, second=28, microsecond=21)
    rounded_date = CronScheduler._round_down_to_nearest_minute(non_rounded_date)
    expected_date = datetime.datetime(year=2020, month=8, day=15, hour=12, minute=24, second=0, microsecond=0)
    assert expected_date == rounded_date

    non_rounded_date = datetime.datetime(year=2024, month=7, day=16, hour=18, minute=45, second=15, microsecond=42214)
    rounded_date = CronScheduler._round_down_to_nearest_minute(non_rounded_date)
    expected_date = datetime.datetime(year=2024, month=7, day=16, hour=18, minute=45, second=0, microsecond=0)
    assert expected_date == rounded_date


def test_time_for_execution_minutely():
    # Every minute a certain task should be performed
    cron_string = "*/1 * * * *"
    initial_datetime = datetime.datetime(year=2020, month=9, day=1, hour=13, minute=23, second=4)
    ten_next_execution_times = [
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=23, second=4),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=24, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=25, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=26, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=27, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=28, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=29, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=30, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=31, second=0),
        datetime.datetime(year=2020, month=9, day=1, hour=13, minute=32, second=0),
    ]

    n = 0
    with freeze_time(initial_datetime) as frozen_datetime:
        scheduler = CronScheduler(cron_string)

        while is_run_condition(n):
            if scheduler.time_for_execution():
                assert datetime.datetime.now() == ten_next_execution_times[n]
                n += 1
            frozen_datetime.tick(1)


def test_time_for_execution_complicated_cron():
    # More complicated scheduling: At every 5th minute past every hour from 1 through 6 on every day-of-week from
    # Tuesday through Thursday in March.
    cron_string = "*/5 1-6 * 3 2-4"

    initial_datetime = datetime.datetime(year=2021, month=2, day=24, hour=9, minute=21, second=46)
    ten_next_execution_times = [
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=0, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=5, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=10, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=15, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=20, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=25, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=30, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=35, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=40, second=0),
        datetime.datetime(year=2021, month=3, day=2, hour=1, minute=45, second=0),
    ]

    n = 0
    with freeze_time(initial_datetime) as frozen_datetime:
        scheduler = CronScheduler(cron_string)

        while is_run_condition(n):
            if scheduler.time_for_execution():
                assert datetime.datetime.now() == ten_next_execution_times[n]
                n += 1
            frozen_datetime.tick(1)


def is_run_condition(n):
    return n < 10
