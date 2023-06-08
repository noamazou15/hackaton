from flask_restx.namespace import Namespace
from flask import session
from flask_restx import Api, Resource

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from enum import Enum

from utils import update_credits 
class Status(Enum):
    WAITING = 'waiting'
    ASSIGNED = 'assigned'
    PICKED_UP = 'picked_up'
    DELIVERED = 'delivered'
    RECEIVED = 'received'



uri = "localhost:27017"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]




ns_packages = Namespace("Packages", description="packages managment", path='/packeges')
@ns_packages.route('/new_package')
class Package(Resource):
    def post(self):
        payload = ns_packages.payload
        pickup = payload.get('pickup')
        dropoff = payload.get('dropoff')
        packageID = payload.get('packageID')
        description = payload.get('description')
        notes = payload.get('extraNotes')
        status = 'waiting'
        user_session = session.get('user_session')
        user_id = mongo_client.users.find_one({'user_session': user_session})['_id']
        mongo_client.packages.insert_one({'pickup_location': pickup,'description':description,
                'dropoff_location': dropoff, 'status':Status.WAITING, 'demanding_user_id': user_id,
                'pickup_user_id':None,
                '_id': packageID, 'notes': notes,'user_session': user_id})
        
        update_credits(user_to_pay=user_id, credits=1)

        return user_session

@ns_packages.route('/my_packages')
class My_package(Resource):
    def get(self):
        user_session = session.get('user_session')
        user_id = mongo_client.users.find_one({'user_session': user_session})['_id']
        packages = mongo_client.packages.find({'demanding_user_id': user_id})
        return list(packages)
    
@ns_packages.route('/my_pickups')
class My_pickups(Resource):
    def get(self):
        user_session = session.get('user_session')
        user_id = mongo_client.users.find_one({'user_session': user_session})['_id']
        packages = mongo_client.packages.find({'pickup_user_id': user_id})
        return list(packages)



@ns_packages.route('/update')
class Update(Resource):
    def post(self):
        payload = ns_packages.payload
        packageID = payload.get('packageID')
        status = payload.get('status')
        user_session = session.get('user_session')
        user_id = mongo_client.users.find_one({'user_session': user_session})['_id']
        if status == Status.DELIVERED:
            mongo_client.packages.update_one({'_id': packageID}, {'$set': {'status': status}})
            update_credits(user_to_receive=user_id, credits=1)
        elif status == Status.ASSIGNED:
            mongo_client.packages.update_one({'_id': packageID}, {'$set': {'status': status, 'pickup_user_id': user_id}})
        else:
            mongo_client.packages.update_one({'_id': packageID}, {'$set': {'status': status}})
 
        return user_session