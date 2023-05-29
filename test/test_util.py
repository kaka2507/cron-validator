from dateutil import rrule

from cron_validator.util import replace_names, str_to_datetime

tz_name = "Asia/Ho_Chi_Minh"
utc_tz = "UTC"


def test_parse_str_to_dt():
    datetime_str = "2019-04-12 13:00"
    dt_local = str_to_datetime(datetime_str, tz_name)
    assert dt_local.year == 2019
    assert dt_local.month == 4
    assert dt_local.day == 12
    assert dt_local.hour == 13
    assert dt_local.second == 0
    dt_utc = str_to_datetime(datetime_str, utc_tz)
    assert dt_utc.year == 2019
    assert dt_utc.month == 4
    assert dt_utc.day == 12
    assert dt_utc.hour == 13
    assert dt_utc.second == 0
    delta = dt_utc - dt_local
    assert delta.seconds == 7 * 60 * 60


def test_iterator_day():
    dt1_str = "2019-04-12 13:00"
    dt2_str = "2019-04-23 1:00"
    dt1 = str_to_datetime(dt1_str, tz_name)
    dt2 = str_to_datetime(dt2_str, tz_name)
    delta = dt1 - dt2
    assert delta.total_seconds() < 0
    for dt in rrule.rrule(rrule.MINUTELY, dtstart=dt1, until=dt2):
        print(dt)


def test_replace_names():
    assert replace_names("* * * */2,3 6") == "* * * */2,3 6"
    assert replace_names("* * * may fri") == "* * * 5 5"
    assert replace_names("* * * jan-sep,nov mon/2") == "* * * 1-9,11 1/2"
    assert replace_names("* * * feb,aug,oct tue,WED,sAT") == "* * * 2,8,10 2,3,6"
    assert replace_names("* * * MAR-apr thu-fri") == "* * * 3-4 4-5"
    assert replace_names("* * * mAy,jun,JUL-DEC SUN/3") == "* * * 5,6,7-12 0/3"
