from flask import Flask
from flask import request, jsonify, send_from_directory
from pymongo import MongoClient
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

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["test_db"]
test_col = db["items"]


app = Flask(__name__)


@app.route("/")
def serve_home():
    
    return send_from_directory(app.static_folder, "index.html")



@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json() or {}
    name = data.get("itemName")
    desc = data.get("itemDescription")
    if not name:
        return jsonify({"error":"itemName required"}), 400
    res = todo_col.insert_one({"itemName":name,"itemDescription":desc})
    return jsonify({"inserted_id": str(res.inserted_id)}), 201


if __name__ == '__main__':

    app.run(host='0.0.0.0',port=7000,debug=True)
