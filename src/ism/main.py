import logging
from get_method import get_method
from mongodb import get_collection
from tqdm import tqdm


def main():
    # 获取集合
    collection = get_collection()

    # 查找所有记录（示例中假设返回多个记录）
    records = collection.find({"Summary-摘要": {"$exists": True}}, {"_id": 1, "Summary-摘要": 1, "Method-研究方法": 1})
    count = collection.count_documents({})
    
    pbar = tqdm(desc="Processing records", total=count)
    for record in records:
        # 提取方法
        if "Method-研究方法" in list(record.keys()):
            pbar.update(1)
        else:
            try:
                methods = get_method(record["Summary-摘要"])
                # 更新记录
                record.update({"Method-研究方法": methods})
                # 将更新写入数据库
                collection.update_one(
                    {"_id": record["_id"]}, {"$set": {"Method-研究方法": methods}}
                )
                pbar.update(1)
            except Exception as e:
                logging.error(f"Failed to process record {record}: {e}")
                continue
    pbar.close()

if __name__ == "__main__":
    main()
