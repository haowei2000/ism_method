import logging
from pathlib import Path

from tqdm import tqdm

from ism_method.mongodb import get_collection


def txt(directory):
    tex_files = []
    tex_files.extend(iter(Path(directory).rglob("*.txt")))
    return tex_files


def parse_info(text: str) -> dict:
    data = {}
    for line in text.split("\n"):
        line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            data[key] = value.strip()
    return data


def write2col(collection, directory=Path(__file__).parents[2] / "dataset",delete_old=False):
    # Clear the collection before inserting new data
    if delete_old:
        collection.delete_many({})
    else:
        logging.warning("The collection is not cleared before inserting new data.")
    txt_files = txt(directory)
    print(txt_files)
    for txt_file in tqdm(txt_files, desc="Processing files"):
        logging.info(f"Processing file: {txt_file}")
        with open(txt_file, "r", encoding="utf-8") as file:
            content = file.read()
            # Connect to MongoDB
            # Parse the content into a dictionary
            for record in content.split("\n\n"):
                data = parse_info(record)
                # Insert the dictionary into MongoDB
                collection.insert_one(data)
    # Remove duplicates based on the "Title-题名" field
    duplicates = collection.aggregate(
        [
            {
                "$group": {
                    "_id": "$Title-题名",
                    "uniqueIds": {"$addToSet": "$_id"},
                    "count": {"$sum": 1},
                }
            },
            {"$match": {"count": {"$gt": 1}}},
        ]
    )

    for doc in duplicates:
        unique_ids = doc["uniqueIds"]
        # Keep the first document and remove the rest
        for id_to_remove in unique_ids[1:]:
            collection.delete_one({"_id": id_to_remove})


def main():
    logging.basicConfig(level=logging.INFO)
    collection = get_collection()
    write2col(collection, directory="/workspace/project/ism_method/dataset",delete_old=True)
