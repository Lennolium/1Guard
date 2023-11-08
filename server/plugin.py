#!/usr/bin/env python3

"""
plugin.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-07"
__status__ = "Prototype/Development/Production"

# Imports.
import hashlib
import uuid

import requests

from secrets import secrets


# Generate a unique ID and fingerprint for the client plugin to
# authenticate with the API.
def generate_api_creds(api_pwd: str) -> tuple[str, str]:
    unique_id = uuid.getnode()  # Unique ID of the client machine.

    # Combine the unique ID and the API password and hash them.
    fingerprint = f"{api_pwd}${unique_id}"
    fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()

    return str(unique_id), fingerprint_hash


# Mockup plugin code to test the API.
def plugin_mockup(client_id, fingerprint, ip_address, domain):
    # Example data to send to the API.
    data = {
            "client_id": client_id,
            "fingerprint": fingerprint,
            "ip_address": ip_address,
            "domain": domain,
            }

    # API endpoint URL
    api_url = "http://127.0.0.1:5000/analyze"

    try:
        # Sending a POST request to the API
        response = requests.post(api_url, json=data)

        # Handling the API response
        if response.status_code == 200:
            response_data = response.json()
            print("Received data from API:")
            print("Score Readable:", response_data["score_readable"])
            print("User Score Readable:", response_data["user_score_readable"])
        else:
            print("Request failed with status code:", response.status_code,
                  response.text
                  )

    except requests.exceptions.RequestException as e:
        print("Request failed with error:", e)


if __name__ == "__main__":
    # Generate API credentials.
    unique_id, fingerprint_hash = generate_api_creds(secrets.API_PASSWORD)

    # TODO: send unique_id and fingerprint_hash to server for auth.

    plugin_mockup(unique_id, fingerprint_hash, "0.0.0.0",
                  "example.com"
                  )
