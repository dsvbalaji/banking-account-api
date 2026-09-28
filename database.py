from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

database = client["banking_api"]

accounts_collection = database["accounts"]

accounts_collection.create_index(
    "account_number",
    unique=True
)