import os
import uuid

from flask import Flask, url_for
from flask_restx import Api
from flask import session
from flask_restx import Resource, fields, abort
from flask_restx.namespace import Namespace

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


import namespaces

uri = "mongodb+srv://root:root@cluster0.npjz8p7.mongodb.net/"
# Create a new client and connect to the server
mongo_client = MongoClient(uri, server_api=ServerApi('1'))["hackaton"]
ENABLE_SWAGGER = os.environ.get('ENABLE_SWAGGER', True)



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

api.add_namespace(namespaces.packages.ns_packages)
api.add_namespace(namespaces.users.ns)
api.add_namespace(namespaces.places.ns)




if __name__ == "__main__":
    app.run(debug=True)
