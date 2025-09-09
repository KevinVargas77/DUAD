# Admin routes
from flask import Blueprint, request, jsonify, g
from models import User, UserRole, Invoice, Product
from db import db_session
from security import admin_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """
    Get all users (admin only).
    """
    # Optional query parameters for filtering
    email_filter = request.args.get('email')
    role_filter = request.args.get('role')
    
    query = db_session.query(User)
    
    # Apply filters if provided
    if email_filter:
        query = query.filter(User.email.ilike(f'%{email_filter}%'))
    
    if role_filter and role_filter in [UserRole.ADMIN, UserRole.USER]:
        query = query.filter(User.role == role_filter)
    
    # Execute query
    users = query.all()
    
    # Format results
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        })
    
    return jsonify({"users": result}), 200

@bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    Get a specific user by ID (admin only).
    """
    user = db_session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
    }), 200

@bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """
    Get dashboard statistics (admin only).
    """
    # Get total users count
    total_users = db_session.query(func.count(User.id)).scalar()
    
    # Get total products count
    total_products = db_session.query(func.count(Product.id)).scalar()
    
    # Get total invoices count
    total_invoices = db_session.query(func.count(Invoice.id)).scalar()
    
    # Get total sales amount
    total_sales = db_session.query(func.sum(Invoice.total_amount)).scalar() or 0.0
    
    # Get low stock products (quantity < 5)
    low_stock_products = db_session.query(Product).filter(Product.quantity < 5).all()
    low_stock_list = []
    for product in low_stock_products:
        low_stock_list.append({
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity
        })
    
    # Get recent invoices (last 5)
    recent_invoices = db_session.query(Invoice).options(
        joinedload(Invoice.user)
    ).order_by(desc(Invoice.created_at)).limit(5).all()
    
    recent_invoices_list = []
    for invoice in recent_invoices:
        recent_invoices_list.append({
            "id": invoice.id,
            "user_id": invoice.user_id,
            "user_email": invoice.user.email if invoice.user else None,
            "total_amount": float(invoice.total_amount),
            "created_at": invoice.created_at.isoformat()
        })
    
    return jsonify({
        "statistics": {
            "total_users": total_users,
            "total_products": total_products,
            "total_invoices": total_invoices,
            "total_sales": float(total_sales)
        },
        "low_stock_products": low_stock_list,
        "recent_invoices": recent_invoices_list
    }), 200
