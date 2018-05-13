from news_fetcher import *


# Note ideally in production level development, we should use separate queue for testing
def test_handle_message():
    # test take message news_fetcher queue
    msg = scrape_news_queue_client.getMessage()
    if not msg:
        print ('tesing with no message returned, possible no message in queue')
        raise

    # print out msg keys
    print ('check sample message keys')
    print (msg.keys())

    # test against Article
    article = Article(task['url'])
    article.download()
    article.parse()
    task['text'] = article.text
    print ('article text')
    print ('-----------------------------------')
    print (task['text'])

    # test message sent to
    # a better way is to get this message from MQ with a testing MQ
    dedupe_news_queue_client.sendMessage(task)
    print ('test success')


if __name__ == "__main__":
    test_handle_message()