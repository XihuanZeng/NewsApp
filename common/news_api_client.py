import requests
from json import loads

NEWS_API_ENDPOINTS = 'https://newsapi.org/v1/'
# API Key get from newsapi.org your account
NEWS_API_KEY = '5319899350b640d4a4291c2e66c66210'
# this name is defined by NewsAPI
CNN = 'cnn'
ARTICLES_API = 'articles'
DEFAULT_SOURCES = [CNN]
SORT_BY = 'top'



def _buildUrl(endPoints=NEWS_API_ENDPOINTS, apiName=ARTICLES_API):
    return endPoints + apiName


def getNewsFromSources(sources=DEFAULT_SOURCES, sortBy = SORT_BY):
    """
    sources could be ['cnn', 'bbc', 'cnbc']
    """
    articles = []

    # note NewsAPI each time only get 1 source
    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        response = requests.get(_buildUrl(), params=payload)

        if response.reason == 'OK':
            # NewsAPI use unicode encoding
            res_json = loads(response.content.decode('utf-8'))
            if (res_json and res_json['status'] == 'ok' and res_json['source']):
                # source is important in ML and in frontend
                # note here we take object within res_json['articles] and this is pass by reference
                for news in res_json['articles']:
                    news['source'] = res_json['source']
            articles.extend(res_json['articles'])

    return articles