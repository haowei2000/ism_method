import pymongo
import yaml


def load_yaml_config(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_collection():
    config = load_yaml_config("src/ism/config.yaml")
    client = pymongo.MongoClient(config["mongodb"]["url"])
    db = client[config["mongodb"]["database"]]
    collection = db[config["mongodb"]["collection"]]
    return collection