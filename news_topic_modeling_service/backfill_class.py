# this script is to backfill the topic class in the mongodb
# at the beginning the training data is exported from mongodb where the records has no class
# Ideally in a production environment, we should keep 2 dbs, one for the training that has only manually labeled text
# the other has all records where label is predicted by the trained model
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        print(count)
        if 'class' not in news:
            print('Populating classes...')
            description = news['description']
            if description is None:
                description = news['title']
            topic = news_topic_modeling_service_client.classify(description)
            news['class'] = topic
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)