from .. import globalMongoClient
from django.conf import settings
import pymongo


def get_conn(db_name="default"):
    if db_name in globalMongoClient:
        return globalMongoClient[db_name]

    if db_name in settings.MONGO_DB:
        config = settings.MONGO_DB[db_name]
        globalMongoClient[db_name] = pymongo.MongoClient(config['HOST'], config['PORT'])
    else:
        globalMongoClient[db_name] = None

    return globalMongoClient[db_name]


def get_db(db_name="default"):
    client = get_conn(db_name)
    if client:
        config = settings.MONGO_DB[db_name]
        if 'DB' in config and config['DB']:
            return client[config['DB']]
    return None
