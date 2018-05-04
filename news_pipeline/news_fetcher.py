import os
import sys

from newspaper import Article


# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://nybetvtl:QTN3c1uP-hWf-oLyVxIGbui71hXIIxDj@eagle.rmq.cloudamqp.com/nybetvtl'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'news_fetcher'
DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://nybetvtl:QTN3c1uP-hWf-oLyVxIGbui71hXIIxDj@eagle.rmq.cloudamqp.com/nybetvtl'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'news_deduper'

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    # we get task from news_fetcher queue, scrape the web page and 
    # push the news with text to news_dedup queue
    # the news are not in Mongo yet.
    dedupe_news_queue_client.sendMessage(task)

def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()