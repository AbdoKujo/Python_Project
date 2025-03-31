from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from app.services.authorization_service import AuthorizationService
from app.repositories.user_repository import UserRepository

def admin_required(fn=None):
    """Decorator to require admin role for a route"""
    # This allows the decorator to be used with or without parentheses
    if fn is None:
        return lambda f: admin_required(f)
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        
        # Get user from db
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(user_id)
        
        # Check if user is an admin
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def permission_required(permission):
    """Decorator to require specific permission"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_id = claims.get('sub')
                
                if not AuthorizationService.has_permission(user_id, permission):
                    return jsonify(error='Permission denied'), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify(error=str(e)), 401
        return wrapper
    return decorator

def rate_limit(limit, period):
    """Decorator to limit request rate"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # This would be implemented with a proper rate limiting solution
            # For now, we'll just pass through
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def validate_json(*required_fields):
    """Decorator to validate required fields in JSON request"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Check if request has JSON
            if not request.is_json:
                return jsonify({'error': 'Missing JSON in request'}), 400
            
            # Check if required fields are present
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

