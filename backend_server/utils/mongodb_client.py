from pymongo import MongoClient

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = "27017"
## you can have multiple database
DB_NAME = "tap-news"

## client only connect once, every time we call get_db will get the same instance
client = MongoClient('%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT))

## we need to return a db instance
def get_db(db = DB_NAME):
    db = client[db]
    return db
