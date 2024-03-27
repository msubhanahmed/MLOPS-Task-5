from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection details
MONGO_HOST = 'mongo'
MONGO_PORT = 27017
MONGO_DB = 'webapp'
MONGO_COLLECTION = 'users'

# Initialize MongoDB client
client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    # Save data to MongoDB
    user_data = {'name': name, 'email': email}
    result = collection.insert_one(user_data)

    if result.inserted_id:
        return 'Data received and stored successfully!'
    else:
        return 'Failed to store data in the database.'

@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find({}, {'_id': 0}))  # Exclude _id field from the response
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
