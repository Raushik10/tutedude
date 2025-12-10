from flask import request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

#uri = "MONGO_URI"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Test_db"]
test_col = db["items"]

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json() or {}
    name = data.get("itemName")
    desc = data.get("itemDescription")
    if not name:
        return jsonify({"error":"itemName required"}), 400
    res = todo_col.insert_one({"itemName":name,"itemDescription":desc})
    return jsonify({"inserted_id": str(res.inserted_id)}), 201
