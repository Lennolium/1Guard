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
import uuid

import requests

from secrets import secrets

API_LOGIN_URL = "http://127.0.0.1:5000/auth/login"
API_ANALYZE_URL = "http://127.0.0.1:5000/analyze/ask"


def api_call(domain=None, token=None):
    # Authorization by login with username (uuid) and api password.
    try:
        if not token:
            # Hash the API access key.
            password = hashlib.sha256(
                    secrets.API_ACCESS_KEY.encode()
                    ).hexdigest()
            username = uuid.getnode()

            response = requests.post(API_LOGIN_URL, auth=(username,
                                                          password)
                                     )

            if response.status_code == 200:
                response_data = response.json()
                token = response_data.get("token", None)

                return token

            else:
                print("Request failed with status code:", response.status_code,
                      response.text
                      )
                return

        # Authorization by passing the token in the header (needed
        # for every request).
        else:
            headers = {'Authorization': f'Bearer {token}'}

            # Example data to send to the API.
            data = {"domain": domain}

            response = requests.post(API_ANALYZE_URL, headers=headers,
                                     json=data
                                     )

            if response.status_code == 200:
                response_data = response.json()

                return response_data

            else:
                print("Request failed with status code:", response.status_code,
                      response.text
                      )
                return

    except requests.exceptions.RequestException as e:
        print("Request failed with error:", e)
        return


# Mockup plugin code to test the API.
def plugin_mockup(domain):
    # Login to the API and get a token.
    token = api_call()
    print("Received token from /auth/login API:")
    print(token)

    # Analyze the domain and passing the token for authorization.
    data = api_call(domain, token)
    print("Received data from /analyze/ask API:")
    print(data)


if __name__ == "__main__":
    plugin_mockup("example.com")
