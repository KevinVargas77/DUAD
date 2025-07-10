from flask import request, jsonify
from flask.views import MethodView
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "tasks.json")
VALID_STATUSES = {"To Do", "In Progress", "Completed"}

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

def validate_task(data):
    errors = []
    if not data.get("id"):
        errors.append("Missing identifier.")
    if not data.get("title"):
        errors.append("Missing title.")
    if not data.get("description"):
        errors.append("Missing description.")
    if data.get("status") not in VALID_STATUSES:
        errors.append("Invalid status.")
    return errors

class TaskAPI(MethodView):

    def get(self, task_id=None):
        tasks = load_tasks()
        if task_id is not None:
            for task in tasks:
                if task["id"] == task_id:
                    return jsonify(task)
            return jsonify({"error": "Task not found."}), 404

        status_filter = request.args.get("status")
        if status_filter:
            filtered = [t for t in tasks if t["status"] == status_filter]
            return jsonify(filtered)
        return jsonify(tasks)

    def post(self):
        task = request.get_json()
        errors = validate_task(task)
        if errors:
            return jsonify({"errors": errors}), 400

        tasks = load_tasks()
        if any(t["id"] == task["id"] for t in tasks):
            return jsonify({"error": "Task with this ID already exists."}), 400

        tasks.append(task)
        save_tasks(tasks)
        return jsonify({"message": "Task created successfully."}), 201

    def put(self, task_id):
        data = request.get_json()
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task.update(data)
                if errors := validate_task(task):
                    return jsonify({"errors": errors}), 400
                save_tasks(tasks)
                return jsonify({"message": "Task updated successfully."})
        return jsonify({"error": "Task not found."}), 404

    def delete(self, task_id):
        tasks = load_tasks()
        new_tasks = [t for t in tasks if t["id"] != task_id]
        if len(new_tasks) == len(tasks):
            return jsonify({"error": "Task not found."}), 404
        save_tasks(new_tasks)
        return jsonify({"message": "Task deleted successfully."})
