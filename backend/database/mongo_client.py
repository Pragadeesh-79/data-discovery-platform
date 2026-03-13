from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://data-discovery-platform:Pragadeesh79@cluster0.9jrovtp.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

# Disable SSL verification for simple hackathon/local testing
client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True)

db = client["data_discovery_platform"]

def get_db():
    return db

test_collection = db["test_collection"]