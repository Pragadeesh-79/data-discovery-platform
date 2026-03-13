from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://data-discovery-platform:Pragadeesh79@cluster0.9jrovtp.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

db = client["data_discovery_platform"]

test_collection = db["test_collection"]