import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # MongoDB Connection String
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://data-discovery-platform:Pragadeesh79@cluster0.9jrovtp.mongodb.net/")
    
    # Target Database Name
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "data-discovery-platform")
    
config = Config()
