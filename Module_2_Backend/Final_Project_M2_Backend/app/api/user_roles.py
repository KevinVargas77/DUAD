from flask import Blueprint, request, jsonify
import uuid
from app.infra.json_store import read_json, write_json


user_roles_bp = Blueprint('user_roles', __name__, url_prefix='/user_roles')


@user_roles_bp.route('/', methods=['POST'])
def assign_role():
    data = request.get_json()
    user_role = {
        "user_id": data["user_id"],
        "role_id": data["role_id"]
    }
    user_roles = read_json('user_roles.json')
    user_roles.append(user_role)
    write_json('user_roles.json', user_roles)
    return jsonify({"user_role": user_role}), 201


@user_roles_bp.route('/<user_id>', methods=['GET'])
def get_user_roles(user_id):
    user_roles = read_json('user_roles.json')
    roles = [ur for ur in user_roles if ur["user_id"] == user_id]
    return jsonify({"user_roles": roles}), 200s