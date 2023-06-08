import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

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

# Route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)
