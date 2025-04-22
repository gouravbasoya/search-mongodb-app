from fastapi import FastAPI, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Allow all CORS origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# MongoDB connection
client = MongoClient("MONGODB URl")#
db = client["groceries"]
collection = db["products"]

# Helper function to convert ObjectId to string
def convert_objectid(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/search")
def search_products(q: str = Query(..., description="Search in Hindi or English")):
    regex_pattern = re.compile(re.escape(q), re.IGNORECASE)
    results = list(collection.find({"search_tags": {"$in": [regex_pattern]}}))
    
    if results:
        # Convert ObjectId to string
        converted_results = [convert_objectid(doc) for doc in results]
        return {"results": converted_results}
    else:
        return {"message": "No matching products found."}
