import operations

# test mongo connected
# note we need to test two conditions
# 1. when user not in redis
# 2. when user in redis
# can modify USER_NEWS_TIME_OUT_IN_SECONDS
def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('test_user', 1)
    print (len(news))
    assert len(news) > 0
    print ('test_getNewsSummariesForUser_basic passed')

# test pagination
def test_getNewsSummariesForUser_pagniation():
    news_page_1 = operations.getNewsSummariesForUser('test_user', 1)
    news_page_2 = operations.getNewsSummariesForUser('test_user', 2)
    print (len(news_page_1))
    print (len(news_page_2))
    assert len(news_page_1) > 0
    assert len(news_page_2) > 0
    digest_page_1_set = set([x['digest'] for x in news_page_1])
    digest_page_2_set = set([x['digest'] for x in news_page_2])
    assert len(digest_page_1_set.intersection(digest_page_2_set)) == 0
    print ('test_getNewsSummariesForUser_pagination passed')

if __name__ == '__main__':
    test_getNewsSummariesForUser_basic()
    test_getNewsSummariesForUser_pagniation()
