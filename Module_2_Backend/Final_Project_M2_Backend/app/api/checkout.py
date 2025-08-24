from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
from app.infra.json_store import read_json, write_json


checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')


@checkout_bp.route('/orders', methods=['GET'])
def list_orders():
    orders = read_json('orders.json')
    return jsonify({"orders": orders}), 200


@checkout_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = read_json('orders.json')
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify({"order": order}), 200
    return jsonify({"error": "Order not found"}), 404


@checkout_bp.route('/invoices', methods=['GET'])
def list_invoices():
    invoices = read_json('invoices.json')
    return jsonify({"invoices": invoices}), 200


@checkout_bp.route('/invoices/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoices = read_json('invoices.json')
    invoice = next((i for i in invoices if i['id'] == invoice_id), None)
    if invoice:
        return jsonify({"invoice": invoice}), 200
    return jsonify({"error": "Invoice not found"}), 404


@checkout_bp.route('/', methods=['POST'])
def checkout():
    user_id = request.json.get("user_id")
    billing_address = request.json.get("billing_address")
    idempotency_key = request.headers.get("Idempotency-Key")

    """obtiene el valor del header HTTP llamado "Idempotency-Key" que el cliente puede enviar en la petición.
    ¿Para qué sirve?
    El Idempotency-Key es una clave única que el cliente (por ejemplo, el frontend) envía para identificar una operación 
    que no debe ejecutarse dos veces, aunque la petición se repita (por ejemplo, por un doble clic o un error de red)."""
    

    carts = read_json('shopping_carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if not cart or not cart['items']:
        return jsonify({"error": "No active cart with items"}), 400


    if not billing_address:
        return jsonify({"error": "Billing address required"}), 400


    products = read_json('products.json')
    for item in cart['items']:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if not product or not product.get('is_active', True):
            return jsonify({"error": f"Product {item['product_id']} not available"}), 400
        if product['stock'] < item['quantity']:
            return jsonify({"error": f"Not enough stock for {product['name']}"}), 400


    snapshot_items = []
    for item in cart['items']:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        snapshot_items.append({
            "product_id": product['id'],
            "name": product['name'],
            "price": product['price'],
            "quantity": item['quantity']
        })


    for item in cart['items']:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        product['stock'] -= item['quantity']
    write_json('products.json', products)


    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "user_id": user_id,
        "items": snapshot_items,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    orders = read_json('orders.json')
    orders.append(order)
    write_json('orders.json', orders)


    invoice_id = str(uuid.uuid4())
    invoice = {
        "id": invoice_id,
        "order_id": order_id,
        "user_id": user_id,
        "billing_address": billing_address,
        "items": snapshot_items,
        "created_at": datetime.now().isoformat()
    }
    invoices = read_json('invoices.json')
    invoices.append(invoice)
    write_json('invoices.json', invoices)


    payment_id = str(uuid.uuid4())
    payment = {
        "id": payment_id,
        "order_id": order_id,
        "user_id": user_id,
        "method": "SINPE",
        "provider_ref": request.json.get("provider_ref"),
        "created_at": datetime.now().isoformat()
    }
    payments = read_json('payments.json')
    payments.append(payment)
    write_json('payments.json', payments)


    cart['is_active'] = False
    cart['status'] = "finalized"
    cart['closed_at'] = datetime.now().isoformat()
    cart['order_id'] = order_id
    write_json('shopping_carts.json', carts)

    return jsonify({
        "order_id": order_id,
        "invoice_id": invoice_id,
        "payment_id": payment_id,
        "message": "Checkout completed"
    }), 201


@checkout_bp.route('/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get("user_id")
    orders = read_json('orders.json')
    if user_id:
        orders = [o for o in orders if o['user_id'] == user_id]
    return jsonify({"orders": orders}), 200


@checkout_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = read_json('orders.json')
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify({"order": order}), 200
    return jsonify({"error": "Order not found"}), 404


@checkout_bp.route('/users/<user_id>/invoices', methods=['GET'])
def get_user_invoices(user_id):
    invoices = read_json('invoices.json')
    user_invoices = [i for i in invoices if i['user_id'] == user_id]
    return jsonify({"invoices": user_invoices}), 200


@checkout_bp.route('/invoices/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoices = read_json('invoices.json')
    invoice = next((i for i in invoices if i['id'] == invoice_id), None)
    if invoice:
        return jsonify({"invoice": invoice}), 200
    return jsonify({"error": "Invoice not found"}), 404


@checkout_bp.route('/invoices/<invoice_id>/items', methods=['GET'])
def get_invoice_items(invoice_id):
    invoices = read_json('invoices.json')
    invoice = next((i for i in invoices if i['id'] == invoice_id), None)
    if invoice:
        return jsonify({"items": invoice.get("items", [])}), 200
    return jsonify({"error": "Invoice not found"}), 404


@checkout_bp.route('/payments/confirm-sinpe', methods=['POST'])
def confirm_sinpe():
    data = request.get_json()
    payment_id = str(uuid.uuid4())
    payment = {
        "id": payment_id,
        "order_id": data.get("order_id"),
        "user_id": data.get("user_id"),
        "method": "SINPE",
        "provider_ref": data.get("provider_ref"),
        "image_url": data.get("image_url"),  # optional
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    payments = read_json('payments.json')
    payments.append(payment)
    write_json('payments.json', payments)
    return jsonify({"message": "SINPE receipt registered", "payment_id": payment_id}), 201


@checkout_bp.route('/payments/reconcile-excel', methods=['POST'])
def reconcile_excel():

    return jsonify({"message": "Excel processed"}), 201


@checkout_bp.route('/orders/<order_id>/refund', methods=['POST'])
def refund_order(order_id):
    orders = read_json('orders.json')
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404


    products = read_json('products.json')
    for item in order['items']:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            product['stock'] += item['quantity']
    write_json('products.json', products)


    refund_id = str(uuid.uuid4())
    refund = {
        "id": refund_id,
        "order_id": order_id,
        "user_id": order["user_id"],
        "created_at": datetime.now().isoformat(),
        "status": "completed"
    }
    refunds = read_json('refunds.json')
    refunds.append(refund)
    write_json('refunds.json', refunds)


    payments = read_json('payments.json')
    for payment in payments:
        if payment['order_id'] == order_id:
            payment['status'] = "refunded"
    write_json('payments.json', payments)

    order['status'] = "refunded"
    write_json('orders.json', orders)

    return jsonify({"message": "Refund completed", "refund_id": refund_id}), 201