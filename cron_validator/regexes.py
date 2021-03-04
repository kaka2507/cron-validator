import re
from enum import Enum

minute_re = re.compile("{0}|{1}|{2}|{3}|{4}".format("(?P<all>\\*)",
                                                    "(?P<specific>[0-5]?\\d)",
                                                    "(?P<range>[0-5]?\\d-[0-5]?\\d)",
                                                    "(?P<list>[0-5]?\\d(,[0-5]?\\d)+)",
                                                    "(?P<step>(\\*|[0-5]?\\d)/(([0-5]?[1-9])|([1-5]0)))"))

hour_re = re.compile("{0}|{1}|{2}|{3}|{4}".format("(?P<all>\\*)",
                                                  "(?P<specific>[01]?\\d|2[0-3])",
                                                  "(?P<range>([01]?\\d|2[0-3])-([01]?\\d|2[0-3]))",
                                                  "(?P<list>([01]?\\d|2[0-3])(,([01]?\\d|2[0-3]))+)",
                                                  "(?P<step>(\\*|[01]?\\d|2[0-3])/([01]?[1-9]|2[0-3]|10))"))

day_of_month_re = re.compile("{0}|{1}|{2}|{3}|{4}".
                             format("(?P<all>\\*)",
                                    "(?P<specific>[1-2]?[1-9]|[1-3]0|31)",
                                    "(?P<range>([1-2]?[1-9]|[1-3]0|31)-([1-2]?[1-9]|[1-3]0|31))",
                                    "(?P<list>([1-2]?[1-9]|[1-3]0|31)(,([1-2]?[1-9]|[1-3]0|31))+)",
                                    "(?P<step>(\\*|[1-2]?[1-9]|[1-3]0|31)/([1-2]?[1-9]|[1-3]0|31))"))

month_re = re.compile("{0}|{1}|{2}|{3}|{4}".format("(?P<all>\\*)",
                                                   "(?P<specific>[1-9]|1[0-2])",
                                                   "(?P<range>([1-9]|1[0-2])-([1-9]|1[0-2]))",
                                                   "(?P<list>([1-9]|1[0-2])(,([1-9]|1[0-2]))+)",
                                                   "(?P<step>(\\*|[1-9]|1[0-2])/([1-9]|1[0-2]))"))

day_of_week_re = re.compile("{0}|{1}|{2}|{3}|{4}".format("(?P<all>\\*)",
                                                         "(?P<specific>[0-6])",
                                                         "(?P<range>[0-6]-[0-6])",
                                                         "(?P<list>[0-6](,[0-6])+)",
                                                         "(?P<step>(\\*|[0-6])/[1-6])"))

regex_list = [
    minute_re,
    hour_re,
    day_of_month_re,
    month_re,
    day_of_week_re
]


class ElementPart(Enum):
    PART_MINUTE = 1
    PART_HOUR = 2
    PART_DAY_OF_MONTH = 3
    PART_MONTH = 4
    PART_DAY_OF_WEEK = 5


class ElementKind(Enum):
    GROUP_TYPE_ALL = 1
    GROUP_TYPE_SPECIFIC = 2
    GROUP_TYPE_RANGE = 3
    GROUP_TYPE_LIST = 4
    GROUP_TYPE_STEP = 5


class Element(object):
    kind = None
    max_value_map = {
        ElementPart.PART_MINUTE: 59,
        ElementPart.PART_HOUR: 23,
        ElementPart.PART_DAY_OF_MONTH: 31,
        ElementPart.PART_MONTH: 11,
        ElementPart.PART_DAY_OF_WEEK: 6
    }

    def __init__(self, part):
        """

        :param ElementPart part:
        """
        self.part = part

    def _get_value(self, dt):
        """

        :param datetime.datetime dt:
        :return:
        """
        maps = {
            ElementPart.PART_MINUTE: 'minute',
            ElementPart.PART_HOUR: 'hour',
            ElementPart.PART_DAY_OF_MONTH: 'day',
            ElementPart.PART_MONTH: 'month',
        }
        attribute = maps.get(self.part)
        if attribute:
            return dt.__getattribute__(attribute)
        return self._convert_weekday(dt.weekday())

    def match(self, dt):
        """

        :param datetime.datetime dt:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def _convert_weekday(weekday):
        """ converts the weekday from starting from a week starting from Monday to a week starting from Sunday

        For the official crontab documentation (https://man7.org/linux/man-pages/man5/crontab.5.html (2020-09-20)) it
        can be seen that their week starts on Sunday, which means SUN = 0, MON = 1, ..., SAT = 6. However, for the
        package dateutil, which performs the actual scheduling, the week starts on a Monday, which means MON = 1,
        TUE = 2, ..., SUN = 6. Since this package shall imitate the real cron syntax to avoid further confusion, the
        weekday is converted to a week where SUN = 0. Nb. the official cron documentation states that 7 shall also be a
        valid input and be corresponding to SUN leading to a week where MON = 1, TUE = 2, ..., SUN = 7. This method
        respects that, however the regex only allows the maximal input of 6.
        :param weekday: integer representing weekday, assuming MON = 1, TUE = 2, ..., SUN = 6
        :return: integer representing passed weekday, however the week starts on Sunday meaning SUN = 0, MON = 1, ...
        """
        if weekday <= 5:
            weekday_week_starting_sunday = weekday + 1
        else:
            weekday_week_starting_sunday = 0
        return weekday_week_starting_sunday


class MatchAllElement(Element):
    kind = ElementKind.GROUP_TYPE_ALL

    def __init__(self, part, body):
        super().__init__(part)
        if body != '*':
            raise ValueError('MatchAllElement only allow *')

    def match(self, dt):
        return True


class MatchSpecificElement(Element):
    kind = ElementKind.GROUP_TYPE_SPECIFIC

    def __init__(self, part, body):
        super().__init__(part)
        self.value = int(body)

    def match(self, dt):
        if self._get_value(dt) == self.value:
            return True
        return False


class MatchListElement(Element):
    kind = ElementKind.GROUP_TYPE_LIST

    def __init__(self, part, body):
        super().__init__(part)
        possible_values = body.split(',')
        self.values = set()
        for value in possible_values:
            self.values.add(int(value))

    def match(self, dt):
        if self._get_value(dt) in self.values:
            return True
        return False


class MatchRangeElement(Element):
    kind = ElementKind.GROUP_TYPE_RANGE

    def __init__(self, part, body):
        super().__init__(part)
        ranges = body.split('-')
        from_value = int(ranges[0])
        to_value = int(ranges[1])
        self.values = set()
        if from_value <= to_value:
            for i in range(from_value, to_value + 1):
                self.values.add(i)
        else:
            for i in range(from_value, self.max_value_map[self.part] + 1):
                self.values.add(i)
            for i in range(0, to_value + 1):
                self.values.add(i)

    def match(self, dt):
        if self._get_value(dt) in self.values:
            return True
        return False


class MatchStepElement(Element):
    kind = ElementKind.GROUP_TYPE_STEP

    def __init__(self, part, body):
        super().__init__(part)
        step_parts = body.split('/')
        if step_parts[0] == '*':
            from_value = 0
        else:
            from_value = int(step_parts[0])
        step_value = int(step_parts[1])
        self.values = set()
        for i in range(from_value, self.max_value_map[self.part] + 1, step_value):
            self.values.add(i)

    def match(self, dt):
        if self._get_value(dt) in self.values:
            return True
        return False


element_kind_map = {
    'all': MatchAllElement,
    'specific': MatchSpecificElement,
    'range': MatchRangeElement,
    'list': MatchListElement,
    'step': MatchStepElement
}
