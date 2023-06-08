from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "localhost:27017"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]




ns_packages = Namespace("Packages", description="packages managment", path='/')
@ns_packages.route('/new_package')
class Login(Resource):
    def post(self):
        payload = ns_packages.payload
        pickup = payload.get('pickup')
        dropoff = payload.get('dropoff')
        packageID = payload.get('packageID')
        notes = payload.get('extraNotes')
        user_session = session.get('user_session')
        user_id = mongo_client.users.find_one({'user_session': user_session})['_id']
        mongo_client.packages.insert_one({'pickup_location': pickup, 'dropoff_location': dropoff,
                '_id': packageID, 'notes': notes,'user_session': user_id})

        return user_session


