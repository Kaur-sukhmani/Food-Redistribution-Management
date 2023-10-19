from session1 import Food_Contributor
from session3 import MongoDBHelper
from bson.objectid import ObjectId


def main():
    db = MongoDBHelper()
    # food_contributor = Food_Contributor()
    # food_contributor.read_food_contributor()
    # print("vars(NourishContributors)")
    # document = vars(food_contributor)
    # db.insert(document)
    query = {"_id": ObjectId('64db960ffdcfca8e03edd941')}
    document_data_to_update = {'name': 'Nanda', 'phone_no': '9316807340', 'email': 'nanda@gmail.com',
                               'address': 'Ludhiana', 'type': 'supermarket', }
    db.update(document_data_to_update, query)


if __name__ == "__main__":
    main()