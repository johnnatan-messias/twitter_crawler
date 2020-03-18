import tweepy

from gateways import RepositoryRDBMS
from utils import LoggerFactory

from .event_type import EventType

logger = LoggerFactory.get_logger("handler_application")

repository = RepositoryRDBMS.Instance()


class Twitter:
    def __init__(self, n_process=8):
        self.n_process = n_process
        self.curr_token = None
        self.__api = None
        self.__rate_limit = None
        self.__connect()

    def __connect(self):
        self.curr_token = repository.get_access_token()
        auth = tweepy.OAuthHandler(
            self.curr_token['app_key'], self.curr_token['app_secret'])
        auth.set_access_token(
            self.curr_token['user_key'], self.curr_token['user_secret'])
        self.__api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(
        ), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.__rate_limit = self.__api.rate_limit_status()['resources']
        logger.info(f"Twitter connected: {self.curr_token}")

    def get_twitter_api(self, type_):
        if self.__rate_limit[type_['type']][type_['path']]['remaining'] > 10:
            self.__rate_limit[type_['type']][type_['path']]['remaining'] -= 1
        else:
            self.__connect()
            logger.info(f"Twitter re-connected: {self.curr_token}")
        return self.__api

    def search(self, query, lang=None, result_type='mixed', max_id=None):
        api = self.get_twitter_api(type_=EventType.SEARCH_TWEET)
        tweets = api.search(q=query, count=100, lang=lang, result_type=result_type,
                            max_id=max_id)
        return tweets


'''

    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                Common.sleep(15 * 60))

    for tweet in limit_handled(tweepy.Cursor(api.search, q='python until:2016-09-20', count = 20).items()):
        print (tweet.id, tweet.created_at)
'''
