from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required, validate_json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
def get_users():
    """Get all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    result, status_code = UserService.get_all_users(page, per_page)
    return jsonify(result), status_code

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_user(user_id):
    """Get user by ID"""
    result, status_code = UserService.get_user_by_id(user_id)
    return jsonify(result), status_code

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required()
@validate_json('username', 'email', 'password', 'role')
def create_user():
    """Create a new user"""
    data = request.get_json()
    result, status_code = UserService.create_user(data)
    return jsonify(result), status_code

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_user(user_id):
    """Update a user"""
    data = request.get_json()
    
    # Validate that we have at least one field to update
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
        
    admin_id = get_jwt_identity()
    
    # Prevent admins from removing their own admin privileges
    if admin_id == user_id and data.get('role') == 'user' and data.get('is_active') is not False:
        return jsonify({'error': 'Admins cannot remove their own admin privileges'}), 400
    
    result, status_code = UserService.update_user(user_id, data)
    return jsonify(result), status_code

@admin_bp.route('/users/<int:user_id>/activate', methods=['PUT'])
@jwt_required()
@admin_required()
def activate_user(user_id):
    """Activate a user"""
    try:
        current_app.logger.info(f"Activating user {user_id}")
        result, status_code = UserService.update_user(user_id, {'is_active': True})
        return jsonify(result), status_code
    except Exception as e:
        current_app.logger.error(f"Error activating user {user_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
@admin_required()
def deactivate_user(user_id):
    """Deactivate a user"""
    try:
        current_app.logger.info(f"Deactivating user {user_id}")
        admin_id = get_jwt_identity()
        
        # Prevent admins from deactivating themselves
        if admin_id == user_id:
            return jsonify({'error': 'Admins cannot deactivate their own account'}), 400
        
        result, status_code = UserService.update_user(user_id, {'is_active': False})
        return jsonify(result), status_code
    except Exception as e:
        current_app.logger.error(f"Error deactivating user {user_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_user(user_id):
    """Delete a user"""
    try:
        current_app.logger.info(f"Deleting user {user_id}")
        admin_id = get_jwt_identity()
        
        # Prevent admins from deleting themselves
        if admin_id == user_id:
            return jsonify({'error': 'Admins cannot delete their own account'}), 400
        
        result, status_code = UserService.delete_user(user_id)
        return jsonify(result), status_code
    except Exception as e:
        current_app.logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

