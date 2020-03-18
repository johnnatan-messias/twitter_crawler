from .pipeline_seach_tweets import TweetSearch


class PipelineFactory:

    @staticmethod
    def crawl_tweets(query, lang=None, result_type='mixed'):
        crawler = TweetSearch(query=query, lang=lang)
        crawler.execute()
