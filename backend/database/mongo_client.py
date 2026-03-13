from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from backend.config import config
import logging

logger = logging.getLogger(__name__)

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        """Initializes the MongoDB connection."""
        if self.client is None:
            try:
                self.client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
                # Verify the connection
                self.client.admin.command('ping')
                self.db = self.client[config.MONGO_DB_NAME]
                logger.info(f"Successfully connected to MongoDB at database: {config.MONGO_DB_NAME}")
                print(f"Successfully connected to MongoDB database '{config.MONGO_DB_NAME}'")
            except ConnectionFailure as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                print(f"Failed to connect to MongoDB: {e}")
                self.client = None
                self.db = None
                raise

    def get_db(self):
        """Returns the database instance. Connects if not already connected."""
        if self.db is None:
            self.connect()
        return self.db

    def get_collection(self, collection_name: str):
        """Returns a specific collection from the database."""
        db = self.get_db()
        return db[collection_name]

    def close(self):
        """Closes the MongoDB connection."""
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("MongoDB connection closed.")

# Singleton instance for easy import
mongo_db = MongoDBClient()

def get_db():
    """Helper function to get the database instance."""
    return mongo_db.get_db()

def get_collection(collection_name: str):
    """Helper function to get a specific collection."""
    return mongo_db.get_collection(collection_name)
