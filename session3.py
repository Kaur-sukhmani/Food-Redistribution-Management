import pymongo
import certifi
from tabulate import tabulate

ca = certifi.where()

class MongoDBHelper:
    def __init__(self, collection='NourishContributors'):
        uri = "mongodb+srv://root:root123456@cluster0.yoemesb.mongodb.net/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri, tlsCAFile=ca)
        self.db = client['food_management']
        self.collection = self.db[collection]

    def insert(self, document):
        result = self.collection.insert_one(document)
        print("Document inserted:", result)

    def delete(self, query):
        result = self.collection.delete_one(query)
        print("Document deleted", result)

    def fetch(self, query=""):
        documents = self.collection.find(query)
        return documents

    def update(self, document, query):
        update_query = {'$set': document}
        result = self.collection.update_one(query, update_query)
        print("Updated Document:", result.modified_count)