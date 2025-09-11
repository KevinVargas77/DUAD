# Purchase routes
from flask import Blueprint, request, jsonify, g
from models import Product, Invoice, InvoiceItem
from db import db_session
from security import jwt_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import select

bp = Blueprint('purchase', __name__, url_prefix='/purchase')

@bp.route('', methods=['POST'])
@jwt_required
def create_purchase():
    """
    Create a purchase for the authenticated user. Any authenticated role can purchase.
    """
    data = request.get_json()
    
    # Validate request body
    if not data or 'items' not in data or not isinstance(data['items'], list):
        return jsonify({"error": "Missing or invalid items array"}), 422
    
    items = data['items']
    
    # Validate items list is not empty
    if not items:
        return jsonify({"error": "Items list must not be empty"}), 422
    
    # Validate each item has product_id and quantity
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return jsonify({"error": f"Item at index {i} is not a valid object"}), 422
        
        if 'product_id' not in item:
            return jsonify({"error": f"Item at index {i} is missing product_id"}), 422
        
        if 'quantity' not in item:
            return jsonify({"error": f"Item at index {i} is missing quantity"}), 422
        
        try:
            # Validate product_id is an integer
            product_id = int(item['product_id'])
            item['product_id'] = product_id
        except ValueError:
            return jsonify({"error": f"Item at index {i} has invalid product_id"}), 422
        
        try:
            # Validate quantity is a positive integer
            quantity = int(item['quantity'])
            if quantity <= 0:
                return jsonify({"error": f"Item at index {i} has invalid quantity (must be > 0)"}), 422
            item['quantity'] = quantity
        except ValueError:
            return jsonify({"error": f"Item at index {i} has invalid quantity"}), 422
    
    # Get current user ID from JWT token
    buyer_user_id = g.user_id
    
    # Merge duplicate product_ids by summing quantities
    merged_items = {}
    for item in items:
        product_id = item['product_id']
        quantity = item['quantity']
        
        if product_id in merged_items:
            merged_items[product_id] += quantity
        else:
            merged_items[product_id] = quantity
    
    # Start transaction
    try:
        with db_session.begin():
            # Lock products for update to prevent race conditions
            product_ids = list(merged_items.keys())
            
            # Use select with for_update to lock rows
            stmt = select(Product).where(Product.id.in_(product_ids)).with_for_update()
            products = db_session.execute(stmt).scalars().all()
            
            # Check if all products exist
            found_product_ids = {p.id for p in products}
            missing_product_ids = set(product_ids) - found_product_ids
            
            if missing_product_ids:
                return jsonify({
                    "error": "Some products not found",
                    "product_ids": list(missing_product_ids)
                }), 404
            
            # Check if all products have sufficient stock
            insufficient_stock = []
            
            for product in products:
                requested_quantity = merged_items[product.id]
                
                if requested_quantity > product.quantity:
                    insufficient_stock.append({
                        "product_id": product.id,
                        "requested": requested_quantity,
                        "available": product.quantity
                    })
            
            if insufficient_stock:
                return jsonify({
                    "error": "Insufficient stock for some products",
                    "items": insufficient_stock
                }), 409
            
            # Create invoice
            invoice = Invoice(
                user_id=buyer_user_id,
                total_amount=0.0  # Will be calculated below
            )
            
            db_session.add(invoice)
            db_session.flush()  # To get invoice.id
            
            # Create invoice items and update stock
            total_amount = 0.0
            
            for product in products:
                quantity = merged_items[product.id]
                unit_price = float(product.price)
                line_total = unit_price * quantity
                
                # Create invoice item
                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total
                )
                
                db_session.add(invoice_item)
                
                # Update product stock
                product.quantity -= quantity
                
                # Add to total amount
                total_amount += line_total
            
            # Update invoice total
            invoice.total_amount = total_amount
            
            # Commit happens automatically at the end of the with block
            
            # Refresh the invoice to load related items
            db_session.refresh(invoice)
            
            # Prepare response
            invoice_items = []
            for item in invoice.items:
                invoice_items.append({
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "line_total": float(item.line_total)
                })
            
            return jsonify({
                "id": invoice.id,
                "user_id": invoice.user_id,
                "total_amount": float(invoice.total_amount),
                "created_at": invoice.created_at.isoformat(),
                "items": invoice_items
            }), 201
            
    except IntegrityError:
        # This will be caught by the with block and automatically rolled back
        return jsonify({"error": "Database integrity error occurred"}), 500
    except SQLAlchemyError as e:
        # This will be caught by the with block and automatically rolled back
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        # This will be caught by the with block and automatically rolled back
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
