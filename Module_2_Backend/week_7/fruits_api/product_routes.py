# Product routes
from flask import Blueprint, request, jsonify, g
from models import Product
from db import db_session
from security import jwt_required, admin_required
from datetime import datetime
from sqlalchemy.exc import IntegrityError

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('', methods=['GET'])
def get_products():
    # Optional query parameters for filtering
    name_filter = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    query = db_session.query(Product)
    
    # Apply filters if provided
    if name_filter:
        query = query.filter(Product.name.ilike(f'%{name_filter}%'))
    
    if min_price:
        try:
            min_price = float(min_price)
            query = query.filter(Product.price >= min_price)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            query = query.filter(Product.price <= max_price)
        except ValueError:
            pass
    
    # Execute query and get results
    products = query.all()
    
    # Format results
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "entry_date": product.entry_date.isoformat()
        })
    
    return jsonify({"products": result}), 200

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db_session.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify({
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "entry_date": product.entry_date.isoformat(),
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat()
        }
    }), 200

@bp.route('', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'price', 'quantity', 'entry_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate data types
    try:
        price = float(data['price'])
        quantity = int(data['quantity'])
        
        # Parse entry_date
        try:
            entry_date = datetime.fromisoformat(data['entry_date'])
        except ValueError:
            return jsonify({"error": "Invalid entry_date format, use ISO format (YYYY-MM-DD)"}), 400
        
        # Create new product
        new_product = Product(
            name=data['name'],
            price=price,
            quantity=quantity,
            entry_date=entry_date
        )
        
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)
        
        return jsonify({
            "message": "Product created successfully",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "price": new_product.price,
                "quantity": new_product.quantity,
                "entry_date": new_product.entry_date.isoformat(),
                "created_at": new_product.created_at.isoformat(),
                "updated_at": new_product.updated_at.isoformat()
            }
        }), 201
        
    except ValueError:
        return jsonify({"error": "Invalid data types. Price must be a number and quantity must be an integer"}), 400
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "An error occurred while creating the product"}), 500
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    product = db_session.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    try:
        if 'name' in data:
            product.name = data['name']
        
        if 'price' in data:
            product.price = float(data['price'])
        
        if 'quantity' in data:
            product.quantity = int(data['quantity'])
        
        if 'entry_date' in data:
            try:
                product.entry_date = datetime.fromisoformat(data['entry_date'])
            except ValueError:
                return jsonify({"error": "Invalid entry_date format, use ISO format (YYYY-MM-DD)"}), 400
        
        db_session.commit()
        db_session.refresh(product)
        
        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "entry_date": product.entry_date.isoformat(),
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat()
            }
        }), 200
        
    except ValueError:
        return jsonify({"error": "Invalid data types. Price must be a number and quantity must be an integer"}), 400
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "An error occurred while updating the product"}), 500
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    product = db_session.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    try:
        db_session.delete(product)
        db_session.commit()
        
        return jsonify({
            "message": "Product deleted successfully"
        }), 200
        
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Cannot delete product because it is referenced by other records"}), 409
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
