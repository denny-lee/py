from .util import mongo_tool


class BaseDao:
    # client = None
    db = None
    currdbName = ''
    currCollName = ''

    def __init__(self):
        # self.client = mongo_tool.get_conn()
        self.db = mongo_tool.get_db()

    # def use_db(self, dbName):
    #     if not self.client:
    #         print('Client not connected.')
    #         return
    #     self.db = self.client[dbName]
    #     self.currdbName = dbName

    # def show_db(self):
    #     print(self.currdbName)
    #     return self.currdbName

    def save(self, model):
        assert self.db, 'No DB Connection'
        if model is None:
            return False
        assert model.get_coll(), 'Check Model.There\'s not collection Defined'
        if not model.checkRequired():
            print('check failed: %s' % model)
            return False
        try:
            if vars(model)['_id'] is None:
                model.set_dates()
                self.db[model.get_coll()].insert_one(vars(model))
            else:
                model.update_dt()
                self.db[model.get_coll()].update_one({"_id":vars(model)['_id']}, {"$set": vars(model)})
            return True
        except Exception as e:
            print(e)
            return False

    def find_all(self, coll):
        assert self.db, 'No DB Connection'
        if not coll:
            return []
        return self.db[coll].find()

    def find_by_id(self, coll, oid):
        assert self.db, 'No DB Connection'
        if not coll or not oid:
            return None
        return self.db[coll].find_one({"_id": oid})

    def count(self, coll):
        assert self.db, 'No DB Connection'
        if not coll:
            return 0
        return self.db[coll].count()

    def search(self, coll, query):
        assert self.db, 'No DB Connection'
        if not coll or query is None:
            return []
        return self.db[coll].find(query)

    def remove_one(self, coll, query):
        assert self.db, 'No DB Connection'
        if not coll or query is None:
            return False
        self.db[coll].remove(query)
        return True