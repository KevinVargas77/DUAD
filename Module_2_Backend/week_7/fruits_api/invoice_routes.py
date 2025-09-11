# Invoice routes
from flask import Blueprint, request, jsonify, g
from models import Invoice, InvoiceItem, User, UserRole
from db import db_session
from security import jwt_required, admin_required
from sqlalchemy.orm import joinedload
from sqlalchemy import desc

bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@bp.route('', methods=['GET'])
@jwt_required
def get_invoices():
    """
    Get invoices for the current user.
    Admin users can get all invoices or filter by user_id.
    Regular users can only get their own invoices.
    """
    user_id = g.user_id
    user_role = g.user_role
    
    # Get query parameters
    filter_user_id = request.args.get('user_id')
    
    query = db_session.query(Invoice).options(joinedload(Invoice.items))
    
    # Apply filters based on user role
    if user_role == UserRole.ADMIN:
        # Admin can filter by user_id or get all
        if filter_user_id:
            try:
                filter_user_id = int(filter_user_id)
                query = query.filter(Invoice.user_id == filter_user_id)
            except ValueError:
                return jsonify({"error": "Invalid user_id parameter"}), 400
    else:
        # Regular users can only get their own invoices
        query = query.filter(Invoice.user_id == user_id)
    
    # Sort by creation date (newest first)
    query = query.order_by(desc(Invoice.created_at))
    
    # Execute query
    invoices = query.all()
    
    # Format results
    result = []
    for invoice in invoices:
        invoice_data = {
            "id": invoice.id,
            "user_id": invoice.user_id,
            "total_amount": float(invoice.total_amount),
            "created_at": invoice.created_at.isoformat(),
            "items": []
        }
        
        for item in invoice.items:
            invoice_data["items"].append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "line_total": float(item.line_total)
            })
        
        result.append(invoice_data)
    
    return jsonify({"invoices": result}), 200

@bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required
def get_invoice(invoice_id):
    """
    Get a specific invoice by ID.
    Admin users can get any invoice.
    Regular users can only get their own invoices.
    """
    user_id = g.user_id
    user_role = g.user_role
    
    # Query the invoice with items loaded
    invoice = db_session.query(Invoice).options(joinedload(Invoice.items)).filter(Invoice.id == invoice_id).first()
    
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    # Check permission
    if user_role != UserRole.ADMIN and invoice.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Format result
    items_data = []
    for item in invoice.items:
        items_data.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "line_total": float(item.line_total)
        })
    
    result = {
        "id": invoice.id,
        "user_id": invoice.user_id,
        "total_amount": float(invoice.total_amount),
        "created_at": invoice.created_at.isoformat(),
        "updated_at": invoice.updated_at.isoformat(),
        "items": items_data
    }
    
    return jsonify({"invoice": result}), 200
