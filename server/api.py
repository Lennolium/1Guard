#!/usr/bin/env python3

"""
api.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-06"
__status__ = "Prototype/Development/Production"

# Imports.
import hashlib
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

import controller
from secrets import secrets
from utils import log

# Child logger.
# LOGGER = logging.getLogger(__name__)
# Root logger and log counter. TODO: just for dev.
LOG_COUNT = log.LogCount()
LOGGER = log.create_logger(LOG_COUNT)
LOGGER.setLevel(10)

# Create the Flask application
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)


def check_client_creds(api_pwd: str, unique_id: str, fingerprint_client: str) \
        -> bool:
    # Combine the unique ID and the API password and hash them.
    combined_string = f"{api_pwd}${unique_id}"
    fingerprint_server = hashlib.sha256(combined_string.encode()).hexdigest()

    if fingerprint_server == fingerprint_client:
        return True

    # Authentication failed.
    return False


# Function to implement API throttling.
# (X requests per second -> 1 / X = Y.Y)
def throttle(f):
    last_call = None
    time_interval = 1 / secrets.API_THROTTLE

    @wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal last_call
        now = datetime.now()
        if last_call and now - last_call < timedelta(seconds=time_interval):
            LOGGER.debug(f"Throttling requests from {request.remote_addr}.")

            return jsonify(
                    {"error": "Too many requests. Please try again later."}
                    ), 429
        last_call = now
        return f(*args, **kwargs)

    return wrapper


# API-Endpoint to receive data from the client, verify the identity of
# the client, and forward the data to the controller.
@app.route('/analyze', methods=['POST'])
@throttle
def analyze():
    data = request.get_json()

    # Ensure required data was passed.
    if not all(key in data for key in
               ('client_id', 'fingerprint', 'ip_address', 'domain')
               ):
        LOGGER.debug(f"Missing required data: {data}")
        return jsonify({"error": "Missing required data"}), 400

    # Extract the data from the request.
    client_id = data.get('client_id')
    fingerprint = data.get('fingerprint')
    ip_address = data.get('ip_address')
    domain = data.get('domain')

    if not check_client_creds(secrets.API_PASSWORD, client_id, fingerprint):
        LOGGER.debug(f"Client identity verification failed: {client_id}\n, "
                     f"{fingerprint}\n, {ip_address}."
                     )
        return jsonify({"error": "Client identity verification failed"}), 401

    # Forward the data to the controller.
    response_data = controller.analyze(domain, ip_address, client_id)

    return jsonify(response_data), 200


# TODO: Implement endpoint to send the data to the client plugin.

# TODO: Implement endpoint to receive the user feedback from client.


# Error handling for unsupported requests.
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


# Error handling for general errors.
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# Run the application if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
