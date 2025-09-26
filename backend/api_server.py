from flask import Flask, jsonify
from flask_cors import CORS
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
try:
    myclient = pymongo.MongoClient(os.getenv("MONGO_URL"))
    myDB = myclient[os.getenv("DB")]
    myCol = myDB[os.getenv("COLLECTION")]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

@app.route('/')
def home():
    return "CaSScade API is running!"

@app.route('/leaderboard')
def get_leaderboard():
    try:
        # Get all submissions sorted by score (highest first)
        submissions = list(myCol.find({}, {"_id": 1, "name": 1, "score": 1}).sort("score", -1))

        # Convert ObjectId to string for JSON serialization
        for submission in submissions:
            submission["_id"] = str(submission["_id"])

        return jsonify({"submission": submissions})
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return jsonify({"submission": []})

@app.route('/test-db')
def test_db():
    try:
        # Test database connection
        result = myCol.find_one()
        if result:
            return jsonify({"status": "success", "message": "Database connected and has data"})
        else:
            return jsonify({"status": "success", "message": "Database connected but no data yet"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Starting CaSScade API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
