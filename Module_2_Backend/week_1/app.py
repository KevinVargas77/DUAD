from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "tasks.json")

VALID_STATUSES = {"To Do", "In Progress", "Completed"}

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: Malformed JSON.")
        return []
    except Exception as e:
        print(f"Unexpected error while reading the file: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"Unexpected error while saving tasks: {e}")

def validate_task(data):
    errors = []

    if "id" not in data:
        errors.append("Missing identifier.")
    elif not isinstance(data["id"], int):
        errors.append("ID must be an integer.")

    if not data.get("title"):
        errors.append("Missing title.")
    if not data.get("description"):
        errors.append("Missing description.")
    
    if "status" not in data:
        errors.append("Missing status.")
    elif data["status"] not in VALID_STATUSES:
        errors.append("Invalid status.")

    return errors

# POST /tasks - Create a task
@app.route("/tasks", methods=["POST"])
def create_task():
    task = request.get_json()
    errors = validate_task(task)
    if errors:
        return jsonify({"error": errors}), 400

    tasks = load_tasks()
    if any(t["id"] == task["id"] for t in tasks):
        return jsonify({"error": "Task with this ID already exists."}), 400

    tasks.append(task)
    save_tasks(tasks)
    return jsonify({"message": "Task created successfully."}), 201

# GET /tasks - Get all tasks (with optional filter)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    status_filter = request.args.get("status")
    tasks = load_tasks()

    if status_filter:
        filtered = [t for t in tasks if t["status"] == status_filter]
        if not filtered:
            return jsonify({"error": f"No tasks found with status '{status_filter}'"}), 404
        return jsonify(filtered)

    return jsonify(tasks)

# PUT /tasks/<id> - Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            found = True
            updated_task = task.copy()
            updated_task.update(data)

            if errors := validate_task(updated_task):
                return jsonify({"error": errors}), 400

            task.update(data)
            break

    if not found:
        return jsonify({"error": "Task not found."}), 404

    save_tasks(tasks)
    return jsonify({"message": "Task updated successfully."})

# DELETE /tasks/<id> - Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found."}), 404

    save_tasks(new_tasks)
    return jsonify({"message": "Task deleted successfully."})

if __name__ == "__main__":
    app.run(debug=True)
