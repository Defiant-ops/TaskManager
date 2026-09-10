from flask import Flask, redirect, request, jsonify, send_from_directory, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask.cli import load_dotenv
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


# =========================================================
# GOOGLE LOGIN
# =========================================================

@app.route("/login")
def login():
    return google.authorize_redirect(
        redirect_uri="http://127.0.0.1:5000/authorize"
    )


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user = token["userinfo"]

    session["user"] = {
        "email": user["email"],
        "name": user.get("name", user["email"])
    }

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/me")
def me():
    if "user" not in session:
        return jsonify({
            "authenticated": False
        }), 401

    return jsonify({
        "authenticated": True,
        "user": session["user"]
    }), 200


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({
                "error": "Unauthorized"
            }), 401

        return f(*args, **kwargs)

    return decorated


# =========================================================
# FRONTEND
# =========================================================

@app.route("/")
def serve_frontend():
    return send_from_directory("static", "index.html")


# =========================================================
# CREATE TASK
# =========================================================

@app.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    description = data.get("description") or ""
    due_date = data.get("dueDate")
    reminder = data.get("reminder") or ""
    status = data.get("status", "pending")

    if not title:
        return jsonify({
            "error": "Task title is required"
        }), 400

    if status not in ("pending", "done"):
        status = "pending"

    if due_date:
        try:
            datetime.fromisoformat(due_date)
        except ValueError:
            return jsonify({
                "error": "Invalid dueDate format, use YYYY-MM-DDTHH:MM"
            }), 400

    task = {
        "title": title,
        "description": description,
        "dueDate": due_date,
        "reminder": reminder,
        "status": status,
        "userEmail": session["user"]["email"]
    }

    result = mongo.db.tasks.insert_one(task)

    return jsonify({
        "id": str(result.inserted_id)
    }), 201


# =========================================================
# GET ALL TASKS
# =========================================================

@app.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = []
    user_email = session["user"]["email"]

    for task in mongo.db.tasks.find({"userEmail": user_email}):
        tasks.append({
            "id": str(task["_id"]),
            "title": task.get("title"),
            "description": task.get("description"),
            "dueDate": task.get("dueDate"),
            "reminder": task.get("reminder"),
            "status": task.get("status", "pending")
        })

    return jsonify(tasks), 200


# =========================================================
# GET SINGLE TASK
# =========================================================

@app.route("/tasks/<id>", methods=["GET"])
@login_required
def get_task(id):
    try:
        task = mongo.db.tasks.find_one({
            "_id": ObjectId(id),
            "userEmail": session["user"]["email"]
        })

        if not task:
            return jsonify({
                "error": "Task not found"
            }), 404

        return jsonify({
            "id": str(task["_id"]),
            "title": task.get("title"),
            "description": task.get("description"),
            "dueDate": task.get("dueDate"),
            "reminder": task.get("reminder"),
            "status": task.get("status", "pending")
        }), 200

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400


# =========================================================
# UPDATE TASK
# =========================================================

@app.route("/tasks/<id>", methods=["PUT"])
@login_required
def update_task(id):
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    description = data.get("description") or ""
    due_date = data.get("dueDate")
    reminder = data.get("reminder") or ""
    status = data.get("status", "pending")

    if not title:
        return jsonify({
            "error": "Task title is required"
        }), 400

    if status not in ("pending", "done"):
        return jsonify({
            "error": "Invalid status"
        }), 400

    if due_date:
        try:
            datetime.fromisoformat(due_date)
        except ValueError:
            return jsonify({
                "error": "Invalid dueDate format, use YYYY-MM-DDTHH:MM"
            }), 400

    try:
        result = mongo.db.tasks.update_one(
            {
                "_id": ObjectId(id),
                "userEmail": session["user"]["email"]
            },
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "dueDate": due_date,
                    "reminder": reminder,
                    "status": status
                }
            }
        )

        if result.matched_count == 0:
            return jsonify({
                "error": "Task not found"
            }), 404

        return jsonify({
            "message": "Task updated"
        }), 200

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400


# =========================================================
# DELETE TASK
# =========================================================

@app.route("/tasks/<id>", methods=["DELETE"])
@login_required
def delete_task(id):
    try:
        result = mongo.db.tasks.delete_one({
            "_id": ObjectId(id),
            "userEmail": session["user"]["email"]
        })

        if result.deleted_count == 0:
            return jsonify({
                "error": "Task not found"
            }), 404

        return jsonify({
            "message": "Task deleted"
        }), 200

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
