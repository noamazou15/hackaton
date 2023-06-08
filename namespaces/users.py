from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "localhost:27017"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]



ns = Namespace("Users", description="users", path='/users')
@ns.route('/credits')
class Credits(Resource):
    def get(self):
        payload = ns.payload
        user_session = payload.get('user_session')
        credits = mongo_client.users.find_one({'user_session': user_session})['credits']

        return credits
    
    def post(self):
        payload = ns.payload
        user_session = payload.get('user_session')
        credits = payload.get('credits')
        curr_credits = mongo_client.users.find_one({'user_session': user_session})['credits']
        if (credits + curr_credits) > 0:
            ns.abort(400, "You don't have enough credits")
        else:
            mongo_client.users.update_one({'user_session': user_session}, {'$set': {'credits': credits}})

        return credits
