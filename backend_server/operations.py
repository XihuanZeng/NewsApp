import json
import os
import sys
import redis
import pickle
from bson.json_util import dumps
from datetime import datetime
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

# server send batch size
NEWS_LIST_BATCH_SIZE = 10
# max number of news fetch from Mongo
NEWS_LIMIT = 200
USER_NEWS_TIME_OUT_IN_SECONDS = 60
# this is not the database name. which is tap-news
# here it is using the news collection. or table
NEWS_TABLE_NAME = "news"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
# redis access db by index db=0
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

LOG_CLICK_TASK_QUEUE_URL = ''
LOG_CLICK_TASK_QUEUE_NAME = ''

# TODO
cloudamqp_client = None

## hello world API
def add(num1, num2):
    print ('add is called with %s and %s' % (num1, num2))
    return num1 + num2

def getOneNews():
    print ('getOneNews is called')
    # random find one
    res = mongodb_client.get_db()['news'].find_one()
    return json.loads(dumps(res))

def getNewsSummariesForUser(user_id, page_number):
    page_number = int(page_number)
    begin_index = (page_number - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_number * NEWS_LIST_BATCH_SIZE

    # final list of news to be returned
    sliced_news = []

    # if redis already have a list of news for user
    # this list is created by recommender engine
    if redis_client.get(user_id) is not None:
        print ('user_id in redis')
        news_digests = pickle.loads(redis_client.get(user_id)) 
        print (len(news_digests))
        # this is just get key, need to go to MongoDB to get value, which is the content of news
        sliced_news_digests = news_digests[begin_index: end_index]
        print (len(sliced_news_digests))
        # Mongo has index on digest, so find is quick
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in':sliced_news_digests}}))
        print (len(sliced_news))
    else:
        print ('user_id not in redis')
        # if not in Redis, call mongo, mongo is user neutral
        db = mongodb_client.get_db()
        # in mongo db we have a list of news
        # we know this is costly, so each user hopefully we only hit this once
        # an optimization is to cache this, but must think of the update frequency of this sorted list
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [x['digest'] for x in total_news]

        # only save digest in Redis, reduce memory of Redis
        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index: end_index]

    # post-process
    for news in sliced_news:
        # in NewsCard, we only show digest of the news, there is no need to show the content
        # we will not deliver all contents since we have limited bandwidth
        # delete text since if user not click it, it is not necessary to show
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'news_id': news_id, 'timestamp': str(datetime.utcnow())}