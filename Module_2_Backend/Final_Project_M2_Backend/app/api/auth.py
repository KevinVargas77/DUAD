import uuid
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from app.infra.json_store import read_json, write_json


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ["email", "password", "name", "last_name"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    users = read_json('users.json')
    if any(u['email'] == data['email'] for u in users):
        return jsonify({"error": "Email already exists"}), 400

    # Campos extra del diagrama
    new_user = {
        "id": str(uuid.uuid4()),
        "email": data["email"],
        "name": data["name"],
        "last_name": data["last_name"],
        "password_hash": data["password"],
        "address": data.get("address", ""),
        "phone": data.get("phone", ""),
        "birth_date": data.get("birth_date", ""),
        "roles": data.get("roles", ["user"]),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    users.append(new_user)
    write_json('users.json', users)
    return jsonify({"message": "User registered successfully", "user": new_user}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    users = read_json('users.json')
    for user in users:
        if user['email'] == data['email'] and user['password_hash'] == data['password']:
            #Note: In a real application, generate and return a JWT token here
            return jsonify({"message": "Login successful", "token": "fake-jwt-token"}), 200
    
    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route('/me', methods=['GET'])
def me():
    #Note: In a real application, you would get the user ID from the JWT token
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    users = read_json('users.json')
    for user in users:
        if user['id'] == user_id:
            # Only return safe fields, not password_hash
            user_copy = user.copy()
            user_copy.pop("password_hash", None)
            return jsonify({"user": user_copy}), 200

    return jsonify({"error": "User not found"}), 404


