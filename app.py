import os
import uuid

from flask import Flask, url_for
from flask_restx import Api
from flask import session
from flask_restx import Resource, fields, abort
from flask_restx.namespace import Namespace
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "localhost:27017"
# Create a new client and connect to the server
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]
ENABLE_SWAGGER = os.environ.get('ENABLE_SWAGGER', False)



app = Flask(__name__)



class AppApi(Api):
    @property
    def specs_url(self):
        """Patch for allowing HTTPS"""
        scheme = 'http' if '5000' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


api = AppApi(version="1.0", title="My API", description="Platform", prefix='/api',
             doc='/doc' if ENABLE_SWAGGER else False,  # doc False to disable Swagger UI
             # security=['basic'], authorizations=authorizations
             )

api.init_app(app, add_specs=ENABLE_SWAGGER)  # add_specs False to disable UI and Swagger.json



ns_packages = Namespace("Packages", description="packages managment", path='/')
api.add_namespace(ns_packages)

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




if __name__ == "__main__":
    app.run(debug=True)
