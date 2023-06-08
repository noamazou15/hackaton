
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId
import json
from math import radians, sin, cos, sqrt, atan2

def is_within_radius(radius, lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth radius in kilometers

    return distance <= radius


uri = "mongodb+srv://root:root@cluster0.npjz8p7.mongodb.net/"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]



def convert_objectid_to_str(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_objectid_to_str(value)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = convert_objectid_to_str(value)
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj

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