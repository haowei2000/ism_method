import pymongo
from ism_method.config import get_config





def get_collection():
    config = get_config()
    client = pymongo.MongoClient(config["mongodb"]["url"])
    db = client[config["mongodb"]["database"]]
    collection = db[config["mongodb"]["collection"]]
    return collection