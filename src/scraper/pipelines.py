from database import get_collection


class MongoPipeLine:
    def __init__(self):
        self.db = get_collection()

    def process_item(self, item, spider):
        print(item)
        self.db.insert_one(item)
