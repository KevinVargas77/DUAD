import os, json
from flask import Blueprint, request, jsonify, url_for
from flask.views import MethodView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE     = os.path.join(BASE_DIR, "tasks.json")
VALID_STATUSES = {"To Do", "In Progress", "Completed"}

# --- Custom Exception ---------------------------------------------------
class DataAccessError(Exception):
    """Raised when the tasks data store is inaccessible or contains invalid JSON."""
    pass

# --- I/O Helpers --------------------------------------------------------
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
        # We don’t have an 'app.logger' here, so just re-raise
        raise DataAccessError("Cannot write to tasks storage.") from e

# --- Validation ---------------------------------------------------------
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

def require_json_body():
    """Return (data, None, None) if valid JSON dict; else (None, response, status)."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, jsonify({"errors": ["Request body must be valid JSON."]}), 400
    return data, None, None

# --- Blueprint & MethodView ---------------------------------------------
task_bp = Blueprint("task_bp", __name__)

@task_bp.errorhandler(DataAccessError)
def handle_data_access_error(error):
    return jsonify({
        "errors": [
            "Internal server error: unable to access tasks. Please try again later."
        ]
    }), 500

class TaskAPI(MethodView):

    def get(self, task_id=None):
        tasks = load_tasks()
        if task_id is not None:
            task = next((t for t in tasks if t["id"] == task_id), None)
            if not task:
                return jsonify({"errors": [f"Task {task_id} not found."]}), 404
            return jsonify(task)

        status = request.args.get("status")
        if status:
            filtered = [t for t in tasks if t["status"] == status]
            if not filtered:
                return jsonify({"errors": [f"No tasks found with status '{status}'."]}), 404
            return jsonify(filtered)

        return jsonify(tasks)

    def post(self):
        data, resp, code = require_json_body()
        if resp:
            return resp, code

        errs = validate_task(data)
        if errs:
            return jsonify({"errors": errs}), 400

        tasks = load_tasks()
        if any(t["id"] == data["id"] for t in tasks):
            return jsonify({"errors": [f"Task {data['id']} already exists."]}), 400

        tasks.append(data)
        save_tasks(tasks)
        return (
            jsonify({"message": "Task created successfully."}),
            201,
            {"Location": url_for("task_bp", task_id=data["id"])}
        )

    def put(self, task_id):
        data, resp, code = require_json_body()
        if resp:
            return resp, code

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return jsonify({"errors": [f"Task {task_id} not found."]}), 404

        updated = {**task, **data}
        errs = validate_task(updated)
        if errs:
            return jsonify({"errors": errs}), 400

        task.update(data)
        save_tasks(tasks)
        return jsonify({"message": "Task updated successfully."})

    def delete(self, task_id):
        tasks = load_tasks()
        new_list = [t for t in tasks if t["id"] != task_id]
        if len(new_list) == len(tasks):
            return jsonify({"errors": [f"Task {task_id} not found."]}), 404

        save_tasks(new_list)
        return "", 204

# register the view on the blueprint
task_view = TaskAPI.as_view("task_bp")
task_bp.add_url_rule("/tasks", defaults={"task_id": None},
                     view_func=task_view, methods=["GET"])
task_bp.add_url_rule("/tasks", view_func=task_view, methods=["POST"])
task_bp.add_url_rule("/tasks/<int:task_id>", view_func=task_view,
                     methods=["GET", "PUT", "DELETE"])
