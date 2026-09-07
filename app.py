from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask.cli import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

# Create task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    dueDate = data.get("dueDate")

    # Validate/parse datetime if provided
    if dueDate:
        try:
            # Expect ISO format: YYYY-MM-DDTHH:MM
            datetime.fromisoformat(dueDate)
        except ValueError:
            return jsonify({"error": "Invalid dueDate format, use YYYY-MM-DDTHH:MM"}), 400

    task = {
        "title": data.get("title"),
        "description": data.get("description"),
        "dueDate": dueDate,                 # full datetime string
        "reminder": data.get("reminder"),   # reminder in D/H/M format
        "status": data.get("status", "pending")
    }
    result = mongo.db.tasks.insert_one(task)
    return jsonify({"id": str(result.inserted_id)}), 201

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = []
    for task in mongo.db.tasks.find():
        tasks.append({
            "id": str(task["_id"]),
            "title": task.get("title"),
            "description": task.get("description"),
            "dueDate": task.get("dueDate"),     # full datetime string
            "reminder": task.get("reminder"),
            "status": task.get("status")
        })
    return jsonify(tasks), 200

# Get single task
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
        if task:
            return jsonify({
                "id": str(task["_id"]),
                "title": task.get("title"),
                "description": task.get("description"),
                "dueDate": task.get("dueDate"),
                "reminder": task.get("reminder"),
                "status": task.get("status")
            }), 200
        return jsonify({"error": "Task not found"}), 404
    except:
        return jsonify({"error": "Invalid task ID"}), 400

# Update task
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.json
    result = mongo.db.tasks.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "title": data.get("title"),
            "description": data.get("description"),
            "dueDate": data.get("dueDate"),
            "reminder": data.get("reminder"),
            "status": data.get("status")
        }}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found"}), 404

# Delete task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
