from flask import Blueprint, request, jsonify
import uuid
from app.infra.json_store import read_json, write_json


roles_bp = Blueprint('roles', __name__, url_prefix='/roles')


@roles_bp.route('/', methods=['GET'])
def get_roles():
    roles = read_json('roles.json')
    return jsonify({"roles": roles}), 200


@roles_bp.route('/', methods=['POST'])
def create_role():
    data = request.get_json()
    role = {
        "id": str(uuid.uuid4()),
        "name": data["name"]
    }
    roles = read_json('roles.json')
    roles.append(role)
    write_json('roles.json', roles)
    return jsonify({"role": role}), 201