from gateways import RepositoryRDBMS
from twitter import Twitter
from utils import Common, FileManager, LoggerFactory, ThreadPool

logger = LoggerFactory.get_logger('logger_application')

repository = RepositoryRDBMS.Instance()


class TweetSearch:
    def __init__(self, query, lang=None, result_type='mixed', n_threads=5):
        self.twitter = Twitter()
        self.query = query
        self.lang = lang
        self.result_type = result_type
        self.tweets = list()
        self.n_threads = n_threads
        self.__n_files = 0
        self.max_id = None

    def execute(self):
        logger.info(
            f"START: crawling tweets -- query={self.query}, lang={self.lang}, result_type={self.result_type}")
        self.__load_last_status()
        self.__crawl_tweets()
        # self.__dump_file(filename='tweets_{}.json.gz')
        logger.info("DONE: crawling tweets")

    def __crawl_tweets(self):
        n_tweets = 0
        n_requests = 1
        logger.info('START: Tweets Crawler')
        if self.max_id is None:
            tweets = self.twitter.search(
                query=self.query, lang=self.lang, result_type=self.result_type)
        else:
            tweets = self.twitter.search(
                query=self.query, lang=self.lang, result_type=self.result_type, max_id=self.max_id-1)
        self.tweets += tweets['statuses']
        max_id = self.tweets[-1]['id']
        n_tweets += len(tweets['statuses'])

        # pool = ThreadPool(num_threads=self.n_threads, save_results=True)
        while 'next_results' in tweets['search_metadata']:
            tweets = self.twitter.search(
                query=self.query, lang=self.lang, result_type=self.result_type, max_id=max_id-1)
            if not tweets['statuses']:
                break
            self.tweets += tweets['statuses']
            max_id = tweets['statuses'][-1]['id']
            n_tweets += len(tweets['statuses'])
            n_requests += 1

            if (n_requests % 1000) == 0:
                self.__n_files += 1
                self.__dump_file(filename=f"tweets_{'-'.join(self.query.split())}_{self.__n_files}.json.gz")
                self.tweets.clear()
                n_requests = 0
            logger.info(
                f"Gathered {n_tweets} tweets: datetime={tweets['statuses'][0]['created_at']} max_id={max_id} n_files={self.__n_files}")
            # pool.add_task(self._crawl_block, block_height)
        # pool.wait_completion()

        logger.info('DONE: Tweets Crawler')

    def __dump_file(self, filename):
        FileManager.dump_json(filename=filename, data=self.tweets)

    def __load_last_status(self):
        logger.info('Loading ids')
        filenames = FileManager.get_dataset_filenames(query='-'.join(self.query.split()))
        if len(filenames) > 0: 
            inFile = FileManager.yield_json_file(filename=filenames[-1])
            for tweet in inFile:
                pass
            self.max_id = tweet['id']
            self.__n_files += len(filenames)
            logger.info(f"Found: id={self.max_id} n_files={self.__n_files} posted on {tweet['created_at']}")


'''
        while 'next_results' in tweets['search_metadata'] and curr_date >= since_datetime:
            response = api.search(q=query, lang=lang, page_=page)
            if not response['statuses']:
                break
            page += 1
            api = self.get_twitter_api(type_=EventType.SEARCH_TWEET)
            curr_date = Common.tweet_time_to_date(
                response['statuses'][-1]['created_at'])
            tweets += response['statuses']
            logger.info(f"Search tweets: current status {curr_date}")
'''
