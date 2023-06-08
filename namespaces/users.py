from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils import convert_objectid_to_str

uri = "mongodb+srv://root:root@cluster0.npjz8p7.mongodb.net/"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]


ns = Namespace("Users", description="users", path='/users')
@ns.route('/credits')
class Credits(Resource):
    def get(self):
        payload = ns.payload
        user_session = payload.get('user_session')
        credits = mongo_client.users.find_one({'user_session': user_session})['credits']
        credits = convert_objectid_to_str(list(credits))
        return credits
    
    def post(self):
        payload = ns.payload
        user_session = session.get('user_session')
        credits = payload.get('credits')
        curr_credits = mongo_client.users.find_one({'user_session': user_session})['credits']
        if (credits == 10000):
            mongo_client.users.update_one({'user_session': user_session}, {'$set': {'credits': 0}})
        if (credits + curr_credits) > 0:
            ns.abort(400, "You don't have enough credits")
        else:
            mongo_client.users.update_one({'user_session': user_session}, {'$set': {'credits': credits}})

        return credits
