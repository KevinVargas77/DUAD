# Authentication routes
from flask import Blueprint, request, jsonify, g
from models import User, UserRole
from db import db_session
from security import hash_password, verify_password, create_token, create_refresh_token, jwt_required, get_current_user
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate email format (simplified)
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate password length
    if len(data['password']) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    # Check if email already exists
    existing_user = db_session.query(User).filter(User.email == data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409
    
    # Set user role (default to USER if not specified or if specified role is invalid)
    role = data.get('role', UserRole.USER)
    if role not in [UserRole.USER, UserRole.ADMIN]:
        role = UserRole.USER
    
    # Create new user
    try:
        hashed_password = hash_password(data['password'])
        new_user = User(
            email=data['email'],
            password_hash=hashed_password,
            role=role
        )
        
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        
        # Generate tokens
        access_token = create_token(new_user.id, new_user.role)
        refresh_token = create_refresh_token(new_user.id, new_user.role)
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "role": new_user.role
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
        
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "An error occurred while registering the user"}), 500
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Find user by email
    user = db_session.query(User).filter(User.email == data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(user.password_hash, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Generate tokens
    access_token = create_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)
    
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required
def me():
    user = get_current_user()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }
    }), 200

@bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.get_json()
    
    if 'refresh_token' not in data:
        return jsonify({"error": "Missing refresh token"}), 400
    
    from security import decode_token
    
    payload = decode_token(data['refresh_token'])
    
    if not payload:
        return jsonify({"error": "Invalid or expired refresh token"}), 401
    
    user_id = int(payload['sub'])
    user_role = payload['role']
    
    # Verify user still exists
    user = db_session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Generate new access token
    access_token = create_token(user_id, user_role)
    
    return jsonify({
        "access_token": access_token
    }), 200
