# this is to clear the unconsunmed cloudAMQP messagess

import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://nybetvtl:QTN3c1uP-hWf-oLyVxIGbui71hXIIxDj@eagle.rmq.cloudamqp.com/nybetvtl'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'news_fetcher'

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://nybetvtl:QTN3c1uP-hWf-oLyVxIGbui71hXIIxDj@eagle.rmq.cloudamqp.com/nybetvtl'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'news_deduper'




# the way is continously getting all messages, so that no one can consume it anymore 
def clearQueue(queue_url, queue_name):
    mq_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if mq_client is not None:
            msg = mq_client.getMessage()
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1

if __name__ == "__main__":
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)