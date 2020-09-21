import datetime

from cron_validator.validator import CronValidator


class CronScheduler(CronValidator):

    def __init__(self, expression):
        super().__init__()
        self.gen = self.get_execution_time(expression, None, None)
        self.next_execution_time = next(self.gen)

    def time_for_execution(self):
        now_rounded = self._round_down_to_nearest_minute(datetime.datetime.now())
        is_time_for_execution = False

        if now_rounded == self.next_execution_time:
            self.next_execution_time = next(self.gen)
            is_time_for_execution = True

        return is_time_for_execution

    @staticmethod
    def _round_down_to_nearest_minute(dt):
        return dt - datetime.timedelta(minutes=dt.minute % 1,
                                       seconds=dt.second,
                                       microseconds=dt.microsecond)