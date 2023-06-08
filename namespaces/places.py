from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "localhost:27017"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]



ns = Namespace("places", description="places", path='/places')

@ns.route('/')
class Places(Resource):
    def get(self):
        places = mongo_client.places.find()
        return list(places)
    