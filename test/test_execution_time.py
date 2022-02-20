from cron_validator import CronValidator
from cron_validator.util import str_to_datetime


def test_generate_execution_time_from_minute_match():
    from_str = "2019-04-23 12:00"
    to_str = "2019-04-23 12:59"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("* * * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 60

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("23 * * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 1
    assert dts[0] == str_to_datetime("2019-04-23 12:23")

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("1,23,59 * * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 3
    assert dts[0] == str_to_datetime("2019-04-23 12:01")
    assert dts[1] == str_to_datetime("2019-04-23 12:23")
    assert dts[2] == str_to_datetime("2019-04-23 12:59")


def test_generate_execution_time_from_hour_match():
    from_str = "2019-04-22 00:00"
    to_str = "2019-04-23 23:59"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 * * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 48

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time(
        "15 0,5,10,15,20 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)
    ):
        print(dt)
        dts.append(dt)
    assert len(dts) == 10

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 */2 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 24

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 1/2 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 24

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 7-9 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 6


def test_generate_execution_time_from_day_of_month_match():
    from_str = "2019-04-22 00:00"
    to_str = "2019-04-23 23:59"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 2

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 22 * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 1

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 22-24 * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 2

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 5 * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 0


def test_generate_execution_time_from_month_match():
    from_str = "2019-04-22 00:00"
    to_str = "2019-04-23 23:59"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 2

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * 4 *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 2

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * 5 *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 0


def test_generate_execution_time_from_day_of_week_match():
    from_str = "2019-04-22 00:00"
    to_str = "2019-04-23 23:59"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 2

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * * 0", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 0

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("0 0 * * 1", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
    assert len(dts) == 1


def test_make_sure_dt_is_rounded():
    from_str = "2019-04-23 12:00:01"
    to_str = "2019-04-23 12:59:02"

    print("--------------------------------------------------")
    dts = list()
    for dt in CronValidator.get_execution_time("* * * * *", from_dt=str_to_datetime(from_str), to_dt=str_to_datetime(to_str)):
        print(dt)
        dts.append(dt)
        assert dt.second == 0
        assert dt.microsecond == 0
    assert len(dts) == 60
