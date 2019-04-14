import datetime
import pytz
import dateutil.parser


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


def str_to_datetime(datetime_str, tz_name='UTC'):
    """

    :param datetime_str:
    :param tz_name:
    :return:
    """
    return dateutil.parser.parse(datetime_str).replace(tzinfo=get_tz(tz_name))
