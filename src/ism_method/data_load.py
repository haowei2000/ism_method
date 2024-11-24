import logging
from pathlib import Path

from tqdm import tqdm

from ism_method.mongodb import get_collection


def get_all_tex_files(directory):
    tex_files = []
    for path in Path(directory).rglob("*.txt"):
        tex_files.append(path)
    return tex_files


def parse_info(text: str) -> dict:
    data = {}
    for line in text.split("\n"):
        line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            data[key] = value.strip()
    return data

def write2col(delete_old=True):
    # Clear the collection before inserting new data
    collection = get_collection()
    if delete_old:
        collection.delete_many({})
    else:
        logging.info("Skipping deletion of old data")
    directory = Path(__file__)/"dataset"
    txt_files = get_all_tex_files(directory)
    for tex_file in tqdm(txt_files, desc="Processing files"):
        with open(tex_file, "r", encoding="utf-8") as file:
            content = file.read()
            # Connect to MongoDB
            # Parse the content into a dictionary
            for record in content.split("\n\n"):
                data = parse_info(record)
                # Insert the dictionary into MongoDB
                collection.insert_one(data)
    # Remove duplicates based on the "Title-题名" field
    duplicates = collection.aggregate([
        {"$group": {
            "_id": "$Title-题名",
            "uniqueIds": {"$addToSet": "$_id"},
            "count": {"$sum": 1}
        }},
        {"$match": {
            "count": {"$gt": 1}
        }}
    ])

    for doc in duplicates:
        unique_ids = doc["uniqueIds"]
        # Keep the first document and remove the rest
        for id_to_remove in unique_ids[1:]:
            collection.delete_one({"_id": id_to_remove})