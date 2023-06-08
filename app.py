import os

from flask import Flask, render_template, send_from_directory, url_for
from flask_restx import Api

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


api = AppApi(version="1.0", title="My API", description="Platform", api_prefix='/api',
             doc='/doc' if ENABLE_SWAGGER else False,  # doc False to disable Swagger UI
             # security=['basic'], authorizations=authorizations
             )

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/packages')
def packages():
    return render_template('packages.html')

@app.route('/newPickupRequest')
def new_pickup_request():
    return render_template('newPickupRequest.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

# Route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

api.init_app(app, add_specs=ENABLE_SWAGGER)  # add_specs False to disable UI and Swagger.json

api.add_namespace(namespaces.packages.ns_packages)
api.add_namespace(namespaces.users.ns)
api.add_namespace(namespaces.places.ns)

if __name__ == "__main__":
    app.run(debug=True)
