from flask import Flask, request, jsonify, url_for
import json
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "tasks.json")

VALID_STATUSES = {"To Do", "In Progress", "Completed"}

class DataAccessError(Exception):
    """
    Raised when the tasks data store is inaccessible
    or contains invalid JSON.
    """
    pass

def load_tasks() -> list[dict]:
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise DataAccessError("Tasks data is corrupted.") from e
    except Exception as e:
        raise DataAccessError("Cannot access tasks storage.") from e

def save_tasks(tasks: list[dict]) -> None:
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        app.logger.error("Failed to write tasks.json", exc_info=e)
        raise DataAccessError("Cannot write to tasks storage.") from e

def validate_task(data: dict) -> list[str]:
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
        errors.append(f"Status must be one of {sorted(VALID_STATUSES)}.")

    return errors

@app.errorhandler(DataAccessError)
def handle_data_access_error(error):
    app.logger.error("Data store failure", exc_info=error)
    return jsonify({
        "errors": ["Internal server error: unable to access tasks. Please try again later."]
    }), 500

def require_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, jsonify({
            "errors": ["Request body must be valid JSON."]
        }), 400
    return data, None, None

# POST /tasks - Create a task
@app.route("/tasks", methods=["POST"])
def create_task():
    data, resp, code = require_json_body()
    if resp:
        return resp, code

    errors = validate_task(data)
    if errors:
        return jsonify({"errors": errors}), 400

    tasks = load_tasks()
    if any(t["id"] == data["id"] for t in tasks):
        return jsonify({"errors": [f"Task with ID {data['id']} already exists."]}), 400

    tasks.append(data)
    save_tasks(tasks)

    return (
        jsonify({"message": "Task created successfully."}),
        201,
        {"Location": url_for("get_task", task_id=data["id"])}
    )

# GET /tasks - Get all tasks (with optional filter)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    status_filter = request.args.get("status")
    tasks = load_tasks()

    if status_filter:
        filtered = [t for t in tasks if t["status"] == status_filter]
        if not filtered:
            return jsonify({
                "errors": [f"No tasks found with status '{status_filter}'."]
            }), 404
        return jsonify(filtered)

    return jsonify(tasks)

# GET /tasks/<id> - Get a single task (for Location URL)
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"errors": [f"Task with ID {task_id} not found."]}), 404

# PUT /tasks/<id> - Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data, resp, code = require_json_body()
    if resp:
        return resp, code

    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"errors": [f"Task with ID {task_id} not found."]}), 404

    updated = {**task, **data}
    errors = validate_task(updated)
    if errors:
        return jsonify({"errors": errors}), 400

    task.update(data)
    save_tasks(tasks)
    return jsonify({"message": "Task updated successfully."})

# DELETE /tasks/<id> - Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"errors": [f"Task with ID {task_id} not found."]}), 404

    save_tasks(new_tasks)
    return "", 204

if __name__ == "__main__":
    app.logger.setLevel("INFO")
    app.run(debug=True)
