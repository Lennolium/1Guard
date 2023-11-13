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
__build__ = "2023.1"
__date__ = "2023-11-07"
__status__ = "Prototype"

# Imports.
import hashlib
import time
import uuid

import requests

from secrets import secrets


# Mockup plugin code to test the API.
def plugin_mockup(domain):
    # Example data to send to the API.

    # API endpoint URL
    api_login_url = "http://127.0.0.1:5000/auth/login"
    api_analyze_url = "http://127.0.0.1:5000/analyze"

    # Login to the API.
    try:
        # Hash the API access key.
        password = hashlib.sha256(
                secrets.API_ACCESS_KEY.encode()
                ).hexdigest()
        username = uuid.getnode()

        response = requests.post(api_login_url, auth=(username,
                                                      password)
                                 )

        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('token', None)
            print("Received data from Login API:")
            print(response.json())

        else:
            print("Request failed with status code:", response.status_code,
                  response.text
                  )
            return

    except requests.exceptions.RequestException as e:
        print("Request failed with error:", e)
        return

    # Example API call.
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(api_analyze_url, headers=headers)
    # response_data = response.json()
    print("Received data from Analyze API:")
    print(response.json())

    time.sleep(3)

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(api_analyze_url, headers=headers)
    # response_data = response.json()
    print("Received data from Analyze API:")
    print(response.json())


if __name__ == "__main__":
    plugin_mockup("example.com")
