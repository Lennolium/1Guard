#!/usr/bin/env python3

"""
secrets.py: TODO: Headline...

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
import const

# Database credentials.
DB_NAME = "1guard_db"
DB_COLLECTION = "website_scores"
DB_URI = (
        "mongodb+srv://1guard-cluster.0s0vyzp.mongodb.net/?authSource"
        "=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority")
DB_CERT = f"{const.APP_PATH}/secrets/X509-cert-3778123170638903818.pem"
DB_RETENTION = 14

# API.
API_USERNAME = "1guard"
API_PASSWORD = "SuperSafePasswordToAccessTheAPI"
API_THROTTLE = 5  # Number of requests per second.
