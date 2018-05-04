import os
import hashlib
import redis
import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import news_api_client
from common.cloudAMQP_client import CloudAMQPClient

# every 10s we use the NewsAPI to fetch news for us
SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3 

NEWS_SOURCES = ['cnn', 'cbc-news', 'financial-times', 'fox-news', 'cnbc', 'fortune',
                'buzzfeed', 'fox-sports', 'google-news', 'espn', 'bbc-news']
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SCARPE_NEWS_QUEUE_URL = 'amqp://nybetvtl:QTN3c1uP-hWf-oLyVxIGbui71hXIIxDj@eagle.rmq.cloudamqp.com/nybetvtl'
SCARPE_NEWS_QUEUE_NAME = 'news_fetcher'
cloudAMQP_client = CloudAMQPClient(SCARPE_NEWS_QUEUE_URL, SCARPE_NEWS_QUEUE_NAME)

def run():
    while True:
        news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)
        num_of_new_news = 0

        # news is one news
        for news in news_list:
            if not news['description']:
                continue
            news_digest = hashlib.md5(news['description'].encode('utf-8')).hexdigest()

            # Redis
            if not redis_client.get(news_digest):
                num_of_new_news += 1
                news['digest'] = news_digest

                # sometimes NewsAPI not having this one
                if not news['publishedAt']:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                
                # key is the hash(description) of the news, and value is a dummy True
                redis_client.set(news_digest, 'True')
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                # put into MQ
                cloudAMQP_client.sendMessage(news)

        print("Fetched %d news" % num_of_new_news)
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    run()