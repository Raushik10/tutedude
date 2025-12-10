from flask import Flask, request, jsonify, render_template

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.test

collection = db['Flask2']




app = Flask(__name__)


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():

    form_data = dict(request.form)

    collection.insert_one(form_data)

    return 'Data submitted succesfully'  

@app.route('/api')
def api():

     data = collection.find()

     data = list(data)

     for item in data:
         print(item)
 
         del item['_id']

        
     data = {
        'data': data
     }    


     return data    




if __name__ == '__main__':

    app.run(debug=True)        
