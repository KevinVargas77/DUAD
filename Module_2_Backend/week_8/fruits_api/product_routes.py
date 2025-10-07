# Product routes - Refactored with Controller and Cache Decorators
from flask import Blueprint, request, jsonify, g
from security import jwt_required, admin_required
from product_controller import ProductController
from cache_decorators import cached_response, invalidate_cache_on_change

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('', methods=['GET'])
@cached_response('all_products')
def get_products():
    """Get all products with optional filters - now with intelligent caching"""
    try:
        # Extract filters from request
        filters = {
            'name': request.args.get('name'),
            'min_price': request.args.get('min_price'),
            'max_price': request.args.get('max_price')
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Get products using controller
        products = ProductController.get_all_products(filters or None)
        
        return jsonify({"products": products}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:product_id>', methods=['GET'])
@cached_response('product')
def get_product(product_id):
    """Get a single product by ID - with caching"""
    try:
        product_data = ProductController.get_product_by_id(product_id)
        
        if not product_data:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify({"product": product_data}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('', methods=['POST'])
@admin_required
@invalidate_cache_on_change(['all_products*'])
def create_product():
    """Create a new product - invalidates relevant caches"""
    data = request.get_json()
    
    try:
        product_data = ProductController.create_product(data)
        
        return jsonify({
            "message": "Product created successfully",
            "product": product_data
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
@invalidate_cache_on_change(['all_products*', 'product*'])
def update_product(product_id):
    """Update an existing product - invalidates relevant caches"""
    data = request.get_json()
    
    try:
        product_data = ProductController.update_product(product_id, data)
        
        if not product_data:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify({
            "message": "Product updated successfully",
            "product": product_data
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
@invalidate_cache_on_change(['all_products*', 'product*'])
def delete_product(product_id):
    """Delete a product - invalidates relevant caches"""
    try:
        success = ProductController.delete_product(product_id)
        
        if not success:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify({
            "message": "Product deleted successfully"
        }), 200
        
    except ValueError as e:
        if "referenced by other records" in str(e):
            return jsonify({"error": str(e)}), 409
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
