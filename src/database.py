import os

import pymongo
from dotenv import load_dotenv

load_dotenv()


def get_collection():
    client = pymongo.MongoClient(os.getenv('MONGO_URL'))
    db = client['course_work']

    collection_name = 'laptops'
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    return db[collection_name]
