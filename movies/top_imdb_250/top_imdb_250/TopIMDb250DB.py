from pymongo import MongoClient

class TopIMDb250DataBase(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['topimdb250_db']
        self.collection = self.db['topimdb250_collect']

    def insertTitle(self, packet):
        self.collection.insert_one(packet)

    def removeAllTitles(self):
        result = self.collection.delete_many({})
        print('Deleted {} Titles from database!'.format(result.deleted_count))

    def getOneTitle(self, **kwargs):
        """
            To find a specific document use something like getOneTitle(**{"user" : "PhillyAdam"})
        """    
        result = self.collection.find_one(kwargs)
        return result

    def getAllTitles(self, **kwargs):
        result = self.collection.find(kwargs)
        return result

    def getNTitles(self, n):
        result = self.collection.find().limit(n)
        return result

    def addNewKey(self, mongo_id, key, **kwargs):
        self.collection.update({ '_id' : mongo_id },  { "$set": { key : kwargs}})

    def close(self):
        self.client.close()
