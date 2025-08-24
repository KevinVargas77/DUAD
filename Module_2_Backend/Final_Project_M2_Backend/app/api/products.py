from flask import Flask, request, jsonify, Blueprint
from app.infra.json_store import read_json, write_json
import uuid
from datetime import datetime


products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    products = read_json('products.json')
    # Validaciones
    if any(p['sku'] == data['sku'] for p in products):
        return jsonify({"error": "SKU already exists"}), 400
    if data.get('price', 0) < 0 or data.get('stock', 0) < 0:
        return jsonify({"error": "Price and stock must be >= 0"}), 400

    new_product = {
        "id": str(uuid.uuid4()),
        "sku": data["sku"],
        "name": data["name"],
        "description": data.get("description", ""),
        "price": data["price"],
        "stock": data["stock"],
        "is_active": True,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    products.append(new_product)
    write_json('products.json', products)
    return jsonify({"message": "Product created", "product": new_product}), 201


@products_bp.route('/', methods=['GET'])
def get_products():
    products = read_json('products.json')
    # Filters
    q = request.args.get('q')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    only_active = request.args.get('only_active')
    if q:
        products = [p for p in products if q.lower() in p['name'].lower() or q.lower() in p.get('description', '').lower()]
    if min_price is not None:
        products = [p for p in products if p.get('price', 0) >= min_price]
    if max_price is not None:
        products = [p for p in products if p.get('price', 0) <= max_price]
    if only_active is not None:
        only_active_bool = str(only_active).lower() == "true"
        products = [p for p in products if p.get('is_active', False) == only_active_bool]
    return jsonify({"products": products}), 200


@products_bp.route('/<identifier>', methods=['GET'])
def get_product(identifier):
    products = read_json('products.json')
    product = next((p for p in products if p['id'] == identifier or p['sku'] == identifier), None)
    if product:
        return jsonify({"product": product}), 200
    return jsonify({"error": "Product not found"}), 404


@products_bp.route('/<product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    products = read_json('products.json')
    for p in products:
        if p['id'] == product_id:
            p['name'] = data.get('name', p['name'])
            p['price'] = data.get('price', p['price'])
            p['stock'] = data.get('stock', p['stock'])
            p['is_active'] = data.get('is_active', p['is_active'])
            write_json('products.json', products)
            return jsonify({"message": "Product updated"}), 200
    return jsonify({"error": "Product not found"}), 404


@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = read_json('products.json')
    for p in products:
        if p['id'] == product_id:
            p['is_active'] = False
            write_json('products.json', products)
            return jsonify({"message": "Product deactivated"}), 200
    return jsonify({"error": "Product not found"}), 404






