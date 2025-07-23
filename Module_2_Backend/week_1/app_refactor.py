from flask import Flask
from views import task_bp

app = Flask(__name__)

# Register our Blueprint
app.register_blueprint(task_bp)

if __name__ == "__main__":
    app.run(debug=True)
