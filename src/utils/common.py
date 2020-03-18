import time

import pytz
from dateutil import parser


class Common:

    @staticmethod
    def get_current_date():
        return time.strftime("%Y-%m-%d")

    @staticmethod
    def tweet_time_to_date(tweet_time):
        dt = parser.parse(tweet_time)
        curr_date = str(dt.astimezone(
            pytz.timezone('America/Sao_Paulo')).date())
        return curr_date

    @staticmethod
    def sleep(time_):
        time.sleep(time_)

