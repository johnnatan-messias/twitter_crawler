import json
import time

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch

from utils import LoggerFactory
from utils.application_paths import ApplicationPaths
from utils.singleton import Singleton

logger = LoggerFactory.get_logger("logger_application")

table_access_token = 'access_token'
table_tweets = 'tweets'

access_tokens_keys = {'id': '%s::INT',
                      'token': '%s::JSONB', 'last_usage': '%s::TEXT'}
tweets_keys = {'id': '%s::INT', 'token': '%s::JSONB', 'last_usage': '%s::TEXT'}


@Singleton
class RepositoryRDBMS:
    __conn = None

    def __init__(self):
        logger.info(">>> Connecting to the database")
        json_str = open(ApplicationPaths.config() + "db_auth.json").read()
        db_auth = json.loads(json_str)
        self.__conn = self.__connect_database(host=db_auth['host'],
                                              port=db_auth['port'],
                                              user=db_auth['user'],
                                              password=db_auth['password'], db=db_auth['db'])
        logger.info(
            f">>> Database {db_auth['db']} connected on server {db_auth['host']}:{db_auth['port']})")

    def __connect_database(self, host, port, user, password, db):
        conn_string = f"host={host} port={port} dbname={db} user={user} password={password}"
        conn = psycopg2.connect(conn_string)
        return conn

    def get_access_token(self):
        sql = f"SELECT id, token::JSON FROM {table_access_token} ORDER BY last_usage LIMIT 1;"
        response = self.__select(sql=sql)
        data = (int(time.time()), response['id'])
        sql = f"UPDATE {table_access_token} SET last_usage = %s WHERE id = %s;"
        self.__persist(sql=sql, data=data)
        return response['token']

    def __select(self, sql, cursor_factory=RealDictCursor):
        response = {}
        try:
            # logger.info(sql)
            cursor = self.__conn.cursor(cursor_factory=cursor_factory)
            cursor.execute(sql)
            response = cursor.fetchone()
        except Exception:
            logger.error('>>> __select', exc_info=True)
        return response

    def __persist(self, sql, data, is_batch=False, page_size=3000):
        try:
            cursor = self.__conn.cursor()
            if is_batch:
                execute_batch(cursor, sql, data, page_size=page_size)
            else:
                cursor.execute(sql, data)
            self.__conn.commit()
        except Exception:
            logger.error('>>> __persist', exc_info=True)
