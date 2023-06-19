import datetime
import re

import dateutil.parser
import pytz

month_names = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
day_of_week_names = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
month_names_re = re.compile(rf"(?<![\d\/])({'|'.join(month_names)})(?!\d)", re.IGNORECASE)
day_of_week_names_re = re.compile(rf"(?<![\d\/])({'|'.join(day_of_week_names)})(?!\d)", re.IGNORECASE)

def get_tz(tz_name):
    """

    :param str tz_name:
    :return:
    """
    # pytz.timezone may return something like +07:07 (Asia/Ho_Chi_Minh)
    # but datetime.datetime will erase the :07 part
    # we need to make them consistent, so always drop :07 part
    _tz = pytz.timezone(tz_name)
    return datetime.datetime.now(tz=_tz).tzinfo


def ts_to_datetime(timestamp_s, tz_name):
    return datetime.datetime.fromtimestamp(timestamp_s, get_tz(tz_name))


def str_to_datetime(datetime_str, tz_name="UTC"):
    """

    :param datetime_str:
    :param tz_name:
    :return:
    """
    return dateutil.parser.parse(datetime_str).replace(tzinfo=get_tz(tz_name))


def replace_names(expression):
    """

    :param expression:
    :return:
    """
    parts = expression.split(" ")
    if len(parts) > 3:
        parts[3] = re.sub(
            month_names_re,
            lambda m: str(month_names.index(m.group().lower()) + 1),
            parts[3]
        )
    if len(parts) > 4:
        parts[4] = re.sub(
            day_of_week_names_re,
            lambda m: str(day_of_week_names.index(m.group().lower())),
            parts[4]
        )
    return " ".join(parts)