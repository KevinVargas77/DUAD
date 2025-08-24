import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.infra.json_store import read_json, write_json


payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.route('/', methods=['POST'])
def create_payment():
    data = request.get_json()
    required = ['order_id', 'invoice_id', 'user_id', 'amount', 'method']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    payments = read_json('payments.json')
    payment = {
        "id": str(uuid.uuid4()),
        "order_id": data['order_id'],
        "invoice_id": data['invoice_id'],
        "user_id": data['user_id'],
        "amount": data['amount'],
        "method": data['method'],
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    payments.append(payment)
    write_json('payments.json', payments)
    return jsonify({"payment": payment}), 201


@payments_bp.route('/', methods=['GET'])
def list_payments():
    payments = read_json('payments.json')
    return jsonify({"payments": payments}), 200


@payments_bp.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payments = read_json('payments.json')
    payment = next((p for p in payments if p['id'] == payment_id), None)
    if payment:
        return jsonify({"payment": payment}), 200
    return jsonify({"error": "Payment not found"}), 404


@payments_bp.route('/<payment_id>', methods=['PATCH'])
def update_payment(payment_id):
    data = request.get_json()
    payments = read_json('payments.json')
    payment = next((p for p in payments if p['id'] == payment_id), None)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    for field in ['status', 'amount', 'method']:
        if field in data:
            payment[field] = data[field]
    payment['updated_at'] = datetime.now().isoformat()
    write_json('payments.json', payments)
    return jsonify({"payment": payment}), 200
