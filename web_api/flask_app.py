import logging
# Flask probably doesn't need to be installed for local development
from flask import Flask, request, Response, jsonify, abort

# For the initial test of hosting the api on pythonanywhere,
# load_synopsis_data is the function that loads 
# SynopticTableModels from json files. For a live site,
# it will either do the same for cached data, or hook to
# the table generator for uncached tables.
from web_api.synopsis_api import load_synopsis_data
from agreement.synoptic_table_model import SynopticTableModel
import json

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Something like this will be needed if the website is hosted outside
# pythonanywhere, such as on GitHub Pages
# from flask-cors import CORS
# CORS(app, resources={r"/*": {"origins": "https://ducknoir.github.io"}})

# This works -- good way to test basic website function.
@app.route('/')
def hello():
    return 'Hello from the Synopsis API!'

# This routes three forms of URI to the endpoint:
# GET https://ducknoir.pythonanywhere.com/get_synopsis/68
# GET https://ducknoir.pythonanywhere.com/get_synopsis?table_name=68
# POST https://ducknoir.pythonanywhere.com/get_synopsis with table_name in JSON request payload
@app.route('/get_synopsis/<table_name>', methods=['GET'])
@app.route('/get_synopsis', methods=['GET', 'POST'])
def get_synopsis(table_name=None):

    if request.method == 'GET':
        # If table_name is not provided in the path, check the query parameters
        if table_name is None:
            table_name = request.args.get('table_name')
            if not table_name:
                abort(400, description="table_name parameter is required")

    elif request.method == 'POST':
        if not request.json or 'table_name' not in request.json:
            abort(400, description="table_name parameter is required")
        table_name = request.json['table_name']

    model_data: SynopticTableModel = load_synopsis_data(table_name)
    response_data = json.dumps(model_data, indent=4, ensure_ascii=False)
    return Response(response_data, mimetype='application/json'), 200
