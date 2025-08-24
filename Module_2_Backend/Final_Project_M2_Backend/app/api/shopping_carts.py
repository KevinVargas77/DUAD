import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.infra.json_store import read_json, write_json


shopping_carts_bp = Blueprint('shopping_carts_bp', __name__, url_prefix='/carts')


@shopping_carts_bp.route('/users/<user_id>/cart', methods=['POST'])
def create_or_get_cart(user_id):
    carts = read_json('shopping_carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if cart:
        return jsonify({"cart": cart}), 200
    created_at = datetime.now().isoformat()
    new_cart = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "is_active": True,
        "status": "active",
        "created_at": created_at,
        "closed_at": None,
        "order_id": None,
        "items": []
    }
    carts.append(new_cart)
    write_json('shopping_carts.json', carts)
    return jsonify({"cart": new_cart}), 201
#Nota: No se si un usuario puede tener un carrito no activo
@shopping_carts_bp.route('/<cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = read_json('shopping_carts.json', cart_id)
    if cart:
        return jsonify(cart), 200
    return jsonify({"error": "Cart not found"}), 404    


@shopping_carts_bp.route('/users/<user_id>/cart', methods=['GET'])
def get_active_cart(user_id):
    carts = read_json('shopping_carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if cart:
        return jsonify({"cart": cart}), 200
    return jsonify({"error": "No active cart"}), 404


@shopping_carts_bp.route('/users/<user_id>/cart/items', methods=['POST'])
def add_item(user_id):
    data = request.get_json()
    quantity = data.get('quantity', 0)
    product_id = data.get('product_id')
    if quantity <= 0:
        return jsonify({"error": "Quantity must be > 0"}), 400

    products = read_json('products.json')
    product = next((p for p in products if p['id'] == product_id and p.get('is_active', True)), None)
    if not product:
        return jsonify({"error": "Product not found or inactive"}), 400
    if product['stock'] < quantity:
        return jsonify({"error": "Not enough stock"}), 400

    carts = read_json('carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if not cart:
        return jsonify({"error": "No active cart"}), 404

    item_id = str(uuid.uuid4())
    cart['items'].append({
        "id": item_id,
        "product_id": product_id,
        "quantity": quantity
    })
    write_json('carts.json', carts)
    return jsonify({"message": "Item added", "item_id": item_id}), 201


@shopping_carts_bp.route('/users/<user_id>/cart/items/<item_id>', methods=['PATCH'])
def update_item(user_id, item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    carts = read_json('carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if not cart:
        return jsonify({"error": "No active cart"}), 404
    for item in cart['items']:
        if item['id'] == item_id:
            if quantity == 0:
                cart['items'].remove(item)
                write_json('carts.json', carts)
                return jsonify({"message": "Item removed"}), 200
            item['quantity'] = quantity
            write_json('carts.json', carts)
            return jsonify({"message": "Item updated"}), 200
    return jsonify({"error": "Item not found"}), 404


@shopping_carts_bp.route('/users/<user_id>/cart/items/<item_id>', methods=['DELETE'])
def delete_item(user_id, item_id):
    carts = read_json('carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if not cart:
        return jsonify({"error": "No active cart"}), 404
    for item in cart['items']:
        if item['id'] == item_id:
            cart['items'].remove(item)
            write_json('carts.json', carts)
            return jsonify({"message": "Item removed"}), 200
    return jsonify({"error": "Item not found"}), 404


@shopping_carts_bp.route('/users/<user_id>/cart', methods=['DELETE'])
def empty_cart(user_id):
    carts = read_json('carts.json')
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('is_active', True)), None)
    if not cart:
        return jsonify({"error": "No active cart"}), 404
    cart['items'] = []
    write_json('carts.json', carts)
    return jsonify({"message": "Cart emptied"}), 200


@shopping_carts_bp.route('/add_item', methods=['POST'])
def add_item_to_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not cart_id or not product_id or quantity < 1:
        return jsonify({"error": "cart_id, product_id y cantidad >= 1 son requeridos"}), 400
    carts = read_json('carts.json')
    products = read_json('products.json')
    cart = next((c for c in carts if c['id'] == cart_id and c['is_active']), None)
    if not cart:
        return jsonify({"error": "Carrito no encontrado o inactivo"}), 404
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    item = {
        "id": str(uuid.uuid4()),
        "cart_id": cart_id,
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": product["price"],
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    cart['items'].append(item)
    cart['updated_at'] = datetime.now().isoformat()
    write_json('carts.json', carts)
    return jsonify({"item": item, "cart": cart}), 201



@shopping_carts_bp.route('/<cart_id>/finalize', methods=['POST'])
def finalize_cart(cart_id):
    carts = read_json('carts.json')
    cart = next((c for c in carts if c['id'] == cart_id and c['is_active']), None)
    if not cart:
        return jsonify({"error": "Carrito no encontrado o inactivo"}), 404
    cart['is_active'] = False
    cart['status'] = "finalized"
    cart['finalized_at'] = datetime.now().isoformat()
    cart['updated_at'] = datetime.now().isoformat()
    write_json('carts.json', carts)
    return jsonify({"message": "Carrito finalizado", "cart": cart}), 200
