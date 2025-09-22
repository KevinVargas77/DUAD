# Contacts routes
from flask import Blueprint, request, jsonify, g
from models import Contact
from db import db_session
from security import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@bp.route('', methods=['GET'])
@jwt_required
def get_contacts():
    """
    Get all contacts for the current user.
    """
    user_id = g.user_id
    
    # Optional query parameter for filtering by name
    name_filter = request.args.get('name')
    
    query = db_session.query(Contact).filter(Contact.user_id == user_id)
    
    # Apply name filter if provided
    if name_filter:
        query = query.filter(Contact.name.ilike(f'%{name_filter}%'))
    
    # Sort by favorite status (favorites first) and then by name
    query = query.order_by(desc(Contact.is_favorite), Contact.name)
    
    # Execute query
    contacts = query.all()
    
    # Format results
    result = []
    for contact in contacts:
        result.append({
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "is_favorite": contact.is_favorite,
            "created_at": contact.created_at.isoformat()
        })
    
    return jsonify({"contacts": result}), 200

@bp.route('/<int:contact_id>', methods=['GET'])
@jwt_required
def get_contact(contact_id):
    """
    Get a specific contact by ID for the current user.
    """
    user_id = g.user_id
    
    contact = db_session.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()
    
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    
    return jsonify({
        "contact": {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "is_favorite": contact.is_favorite,
            "created_at": contact.created_at.isoformat(),
            "updated_at": contact.updated_at.isoformat()
        }
    }), 200

@bp.route('', methods=['POST'])
@jwt_required
def create_contact():
    """
    Create a new contact for the current user.
    """
    user_id = g.user_id
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Get optional fields
    phone = data.get('phone')
    is_favorite = data.get('is_favorite', False)
    
    # Validate email format (simplified)
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400
    
    try:
        # Create new contact
        new_contact = Contact(
            user_id=user_id,
            name=data['name'],
            email=data['email'],
            phone=phone,
            is_favorite=is_favorite
        )
        
        db_session.add(new_contact)
        db_session.commit()
        db_session.refresh(new_contact)
        
        return jsonify({
            "message": "Contact created successfully",
            "contact": {
                "id": new_contact.id,
                "name": new_contact.name,
                "email": new_contact.email,
                "phone": new_contact.phone,
                "is_favorite": new_contact.is_favorite,
                "created_at": new_contact.created_at.isoformat(),
                "updated_at": new_contact.updated_at.isoformat()
            }
        }), 201
        
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "An error occurred while creating the contact"}), 500
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:contact_id>', methods=['PUT'])
@jwt_required
def update_contact(contact_id):
    """
    Update a contact for the current user.
    """
    user_id = g.user_id
    
    contact = db_session.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()
    
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'name' in data:
        contact.name = data['name']
    
    if 'email' in data:
        # Validate email format (simplified)
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400
        contact.email = data['email']
    
    if 'phone' in data:
        contact.phone = data['phone']
    
    if 'is_favorite' in data:
        contact.is_favorite = bool(data['is_favorite'])
    
    try:
        db_session.commit()
        db_session.refresh(contact)
        
        return jsonify({
            "message": "Contact updated successfully",
            "contact": {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "is_favorite": contact.is_favorite,
                "created_at": contact.created_at.isoformat(),
                "updated_at": contact.updated_at.isoformat()
            }
        }), 200
        
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "An error occurred while updating the contact"}), 500
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:contact_id>', methods=['DELETE'])
@jwt_required
def delete_contact(contact_id):
    """
    Delete a contact for the current user.
    """
    user_id = g.user_id
    
    contact = db_session.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()
    
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    
    try:
        db_session.delete(contact)
        db_session.commit()
        
        return jsonify({
            "message": "Contact deleted successfully"
        }), 200
        
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Cannot delete contact because it is referenced by other records"}), 409
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
