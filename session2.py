import pymongo
import certifi

ca = certifi.where()

# uri = "mongodb+srv://root:<root123>@cluster0.yoemesb.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://root:root123456@cluster0.yoemesb.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, tlsCAFile=ca)
db = client['food_management']
collections = db.list_collection_names()
print(collections)
for collection in collections:
    print(collection)

documents = db['NourishContributors'].find()
# to fetch all collections from  documents
for document in documents:
    print(document)

