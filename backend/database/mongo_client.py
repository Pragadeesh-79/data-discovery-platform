"""
MongoDB client configuration for the DPDPA Data Discovery Platform.
This module handles connecting to MongoDB Atlas.
"""

from pymongo import MongoClient
import urllib.parse
import certifi
import os

# 1. MongoDB Atlas Connection String
# URL-encoding the password is required if it contains special characters like @, :, ?, etc.
username = urllib.parse.quote_plus("data-discovery-platform")
password = urllib.parse.quote_plus("Pragadeesh79")

# Use the exact cluster URL with the correct parameters
DEFAULT_MONGODB_URI = f"mongodb+srv://{username}:{password}@cluster0.9jrovtp.mongodb.net/?retryWrites=true&w=majority"
MONGODB_URI = os.getenv("MONGODB_URI", DEFAULT_MONGODB_URI)

# 2. Create a MongoDB client instance
# We add serverSelectionTimeoutMS to fail fast if the connection cannot be established
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=10000,
    connectTimeoutMS=10000,
    tlsCAFile=certifi.where()
)

# 3. Access the specific database named 'data_discovery'
db = client["data_discovery"]

def get_db():
    return db

# 4. References to the required collections
pii_inventory = db["pii_inventory"]
sample_data_sources = db["sample_data_sources"]

def check_db_connection():
    """
    Test the MongoDB connection by issuing a simple 'ping' command.
    Returns True if connected, False otherwise.
    """
    try:
        # The ismaster command is cheap and does not require auth
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False
