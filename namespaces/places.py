from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId
import json
from utils import convert_objectid_to_str


uri = "mongodb+srv://root:root@cluster0.npjz8p7.mongodb.net/"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]



ns = Namespace("places", description="places", path='/places')

@ns.route('/')
class Places(Resource):
    def get(self):
        places = mongo_client.locations.find({"pickup_center": True})
        places = list(places)
        converted_places = convert_objectid_to_str(places)

        return converted_places
    
@ns.route('/pickup')
class Place(Resource):
    def get(self):
        payload = ns.payload
        location = payload.get('id')
        place = mongo_client.packages.find({"pickup_location": location })
        place = convert_objectid_to_str(list(place))
        return place
    