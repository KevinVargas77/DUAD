# Security utilities (authentication, authorization)
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from config import settings
from models import User
from db import db_session
import os

# Load JWT keys
def load_key(path):
    with open(path, 'rb') as file:
        return file.read()

# Load private key for signing JWT tokens
try:
    private_key = load_key(settings.JWT_PRIVATE_KEY_PATH)
except:
    print(f"WARNING: Could not load private key from {settings.JWT_PRIVATE_KEY_PATH}")
    private_key = None

# Load public key for verifying JWT tokens
try:
    public_key = load_key(settings.JWT_PUBLIC_KEY_PATH)
except:
    print(f"WARNING: Could not load public key from {settings.JWT_PUBLIC_KEY_PATH}")
    public_key = None

# Function to create a JWT token
def create_token(user_id, user_role, expires_delta=None):
    if not private_key:
        raise Exception("Private key not loaded. Cannot create token.")
    
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": str(user_id),
        "role": user_role,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, private_key, algorithm=settings.JWT_ALGORITHM)

# Function to create a refresh token
def create_refresh_token(user_id, user_role):
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(user_id, user_role, expires_delta=expires_delta)

# Function to decode a JWT token
def decode_token(token):
    if not public_key:
        raise Exception("Public key not loaded. Cannot verify token.")
    
    try:
        payload = jwt.decode(token, public_key, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to require JWT authentication
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Set user_id in flask g object for route handlers to use
        g.user_id = int(payload['sub'])
        g.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated

# Decorator to require admin role
def admin_required(f):
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        if g.user_role != 'admin':
            return jsonify({"error": "Admin role required"}), 403
        
        return f(*args, **kwargs)
    
    return decorated

# Function to get current user from database based on JWT token
def get_current_user():
    user_id = g.get('user_id')
    if not user_id:
        return None
    
    return db_session.query(User).filter(User.id == user_id).first()

# Password hashing utilities
import hashlib
import os

def hash_password(password):
    """Create a secure hash for a password"""
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac(
        'sha256',           # Hash digest algorithm
        password.encode('utf-8'),  # Convert the password to bytes
        salt,               # Provide the salt
        100000              # Number of iterations of PBKDF2
    )
    # Store the salt with the password
    return salt.hex() + ':' + key.hex()

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password"""
    salt_hex, key_hex = stored_password.split(':')
    salt = bytes.fromhex(salt_hex)
    stored_key = bytes.fromhex(key_hex)
    
    # Use the same hash function to calculate a key based on the provided password
    key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    
    # Compare the calculated key with the stored key
    return key == stored_key
