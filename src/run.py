import argparse
import json

from pipeline import PipelineFactory
from utils import ApplicationPaths, FileManager, LoggerFactory

logger = LoggerFactory.get_logger("logger_application")


def main(args):
    logger.info("START: Main Application")
    ApplicationPaths.makedirs()
    if args.method == 'search':
        PipelineFactory.crawl_tweets(
            query=args.query, lang='pt', result_type='mixed')
    logger.info("END: Main Application")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Twitter crawler')
    parser.add_argument('--method', required=True, type=str, choices=['search'],
                        help='search: Get tweets in respect to a given query'
                        )
    parser.add_argument('--query', type=str, help='Please, specify a query')

    args = parser.parse_args()
    main(args)
