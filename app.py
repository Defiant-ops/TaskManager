from flask import Flask, request, jsonify, send_from_directory
from flask.cli import load_dotenv
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)
tasks_collection = mongo.db.tasks

def validate_id(id):
    return ObjectId.is_valid(id)

# Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "'title' is required and body must be JSON"}), 400

    task_doc = {
        "title": data.get("title"),
        "description": data.get("description", ""),
        "dueDate": data.get("dueDate"),
        "status": data.get("status", "pending")
    }
    task_id = tasks_collection.insert_one(task_doc).inserted_id
    return jsonify({"id": str(task_id)}), 201

# Read All Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = []
    for task in tasks_collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "title": task.get("title"),
            "description": task.get("description"),
            "dueDate": task.get("dueDate"),
            "status": task.get("status")
        })
    return jsonify(tasks), 200

# Read One Task
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    if not validate_id(id):
        return jsonify({"error": "Invalid task ID"}), 400

    task = tasks_collection.find_one({"_id": ObjectId(id)})
    if task:
        return jsonify({
            "id": str(task["_id"]),
            "title": task.get("title"),
            "description": task.get("description"),
            "dueDate": task.get("dueDate"),
            "status": task.get("status")
        }), 200
    return jsonify({"error": "Task not found"}), 404

# Update Task
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    if not validate_id(id):
        return jsonify({"error": "Invalid task ID"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    allowed_fields = ["title", "description", "dueDate", "status"]
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields provided to update"}), 400

    result = tasks_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    if result.matched_count > 0:
        return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found"}), 404

# Delete Task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    if not validate_id(id):
        return jsonify({"error": "Invalid task ID"}), 400

    result = tasks_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')



if __name__ == '__main__':
    app.run(debug=True)