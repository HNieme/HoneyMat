
from flask import Flask, request, jsonify
import configparser

config = configparser.RawConfigParser()
config.read('config.cfg')
details_dict = dict(config.items('SECURITY'))

api_key = details_dict['api_key']


app = Flask(__name__)


@app.route('/dispense', methods=['POST'])
def dispense():
    print("dispense")
    if 'X-API-Key' in request.headers:
        request_api_key = request.headers['X-API-Key']
    else:
        return "Missing api key", 401
    if request_api_key != api_key:
        return "Wrong api key", 401

    data = request.json  # Get the JSON data from the incoming request
    # Process the data and perform actions based on the event

    print(data["honey500"])
    return jsonify({'dispensed': data['honey500']}), 200


@app.route('/healthcheck', methods=['GET'])
def health_check():
    # data = request.json # Get the JSON data from the incoming request
    # Process the data and perform actions based on the event

    print("healthcheck")
    return jsonify({'health': 'ok'}), 200


app.run()
