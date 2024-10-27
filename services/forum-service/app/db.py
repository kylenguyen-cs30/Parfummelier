
# app/db.py
import os
from pymongo import MongoClient
import atexit

# MongoDB connection setup
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/chat_database")
client = MongoClient(mongo_uri)
db = client["chat_database"]

def test_mongodb():
    try:
        # NOTE: Test inserting a document
        result = db.test_collection.insert_one({"name": "test"})
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Test fetching the inserted document
        fetched_doc = db.test_collection.find_one({"name": "test"})
        print(f"Fetched document: {fetched_doc}")
        
        # Clean up the test document
        db.test_collection.delete_one({"name": "test"})
        print("Test document deleted.")
        
    except Exception as e:
        print(f"MongoDB Test Failed: {e}")

# Run the test
test_mongodb()

# Initialize the collections
chatrooms_collection = db["chatrooms"]
messages_collection = db["messages"]

# Ensure MongoDB connection is closed on application exit
atexit.register(client.close)
