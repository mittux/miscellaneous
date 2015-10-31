from pymongo import MongoClient

class TwitterDataBase(object):
    def __init__(self):
        self.client = MongoClient()
        # TODO : check 'serverStatus'
        self.db = self.client['twitter_db']
        self.collection = self.db['twitter_collect']

    def insertTweet(self, packet):
        self.collection.insert_one(packet)

    def removeAllTweets(self):
        result = self.collection.delete_many({})
        print('Deleted {} tweets from database!'.format(result.deleted_count))

    def getOneTweet(self, **kwargs):
        # To find a specific document use something like getOneTweet(**{"user" : "PhillyAdam"})
        result = self.collection.find_one(kwargs)
        return result

    def getAllTweets(self):
        result = self.collection.find({})
        return result

