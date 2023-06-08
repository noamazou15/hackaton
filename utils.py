
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "localhost:27017"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]



def update_credits(user_to_pay=None, user_to_receive=None, credits=0):
    curr_credits = mongo_client.users.find_one({'user_id': user_to_pay})['credits']
    if (credits - curr_credits) > 0:
        return False
    else:
        if (user_to_pay):
            mongo_client.users.update_one({'user_id': user_to_pay}, {'$inc': {'credits': -credits}})
        if (user_to_receive):
            mongo_client.users.update_one({'user_id': user_to_receive}, {'$inc': {'credits': credits}})
        return True