import uuid
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from app.infra.json_store import read_json, write_json


users_bp = Blueprint('users',__name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    users = read_json('users.json')
    return jsonify({"users": users}), 200


@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    users = read_json('users.json')
    for user in users:
        if user['id'] == user_id:
            return jsonify({"user": user}), 200
    return jsonify({"error": "User not found"}), 404
# Note: In a real application, you would get the user ID from the JWT token

@users_bp.route('/<user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()
    users = read_json('users.json')
    for user in users:
        if user['id'] == user_id:
            user['full_name'] = data.get('full_name', user['full_name'])
            write_json('users.json', users)
            return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404


@users_bp.route('/<user_id>/roles', methods=['POST'])
def add_role(user_id):
    data = request.get_json()
    role = data.get('role')
    if not role:
        return jsonify({"error": "Role is required"}), 400
    users = read_json('users.json')
    for user in users:
        if user['id'] == user_id:
            if role not in user['roles']:
                user['roles'].append(role)
                write_json('users.json', users)
            return jsonify({"message": "Role added"}), 200
    return jsonify({"error": "User not found"}), 404


