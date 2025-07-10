from flask import Flask
from views import TaskAPI

print("RUNNING app_refactor.py with MethodView!")

app = Flask(__name__)

task_view = TaskAPI.as_view("task_api")
app.add_url_rule("/tasks", defaults={"task_id": None}, view_func=task_view, methods=["GET"])
app.add_url_rule("/tasks", view_func=task_view, methods=["POST"])
app.add_url_rule("/tasks/<int:task_id>", view_func=task_view, methods=["GET", "PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True)
