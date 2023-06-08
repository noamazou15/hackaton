from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId
import json
from utils import convert_objectid_to_str, is_within_radius


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
        lon = payload.get('lon')
        lat = payload.get('lat')
        radius = payload.get('radius')
        location = ObjectId(payload.get('id'))
        locations = mongo_client.locations.find({"pickup_center": False})
        filtered_locs = []
        for loc in locations:
            place_lat = loc['coordinates']['latitude']
            place_lon = loc['coordinates']['longitude']
            print(is_within_radius(radius, lat, lon, place_lat, place_lon))
            if is_within_radius(radius, lat, lon, place_lat, place_lon):
                filtered_locs.append(loc['_id'])
        
        place_cursor = mongo_client.packages.find({"pickup_location": location,"dropoff_location": {"$in": filtered_locs} })
        place_cursor = list(place_cursor)
        place_cursor = convert_objectid_to_str(place_cursor)

        return place_cursor
    

    