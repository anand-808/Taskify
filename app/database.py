from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "taskify_db")

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

# Get tasks collection
tasks_collection = database.tasks