from flask import Blueprint, request, jsonify, make_response
from app.services.auth_service import AuthService
from app.utils.decorators import validate_json
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@validate_json('username', 'email', 'password')
def register():
    """Register a new user"""
    data = request.get_json()
    result, status_code = AuthService.register(data)
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
@validate_json('username', 'password')
def login():
    """Login a user"""
    data = request.get_json()
    result, status_code = AuthService.login(data)
    
    if status_code == 200:
        # Create response with token in both JSON and cookies
        response = make_response(jsonify(result), status_code)
        
        # Set cookies for server-side auth
        # httponly=True prevents JavaScript from accessing the cookie
        response.set_cookie(
            'access_token', 
            result['access_token'],
            httponly=True,
            secure=request.is_secure,  # True in HTTPS
            samesite='Lax',
            max_age=3600  # 1 hour
        )
        
        return response
    
    return jsonify(result), status_code

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout a user"""
    # Create response
    response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
    
    # Clear the cookie
    response.delete_cookie('access_token')
    
    return response

@auth_bp.route('/refresh', methods=['POST'])
@validate_json('refresh_token')
def refresh():
    """Refresh access token"""
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    result, status_code = AuthService.refresh_token(refresh_token)
    
    if status_code == 200:
        # Create response with token in both JSON and cookies
        response = make_response(jsonify(result), status_code)
        
        # Set cookies for server-side auth
        response.set_cookie(
            'access_token', 
            result['access_token'],
            httponly=True,
            secure=request.is_secure,
            samesite='Lax',
            max_age=3600  # 1 hour
        )
        
        return response
    
    return jsonify(result), status_code

