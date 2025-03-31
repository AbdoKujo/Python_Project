from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import permission_required, validate_json

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    result, status_code = UserService.get_profile(user_id)
    return jsonify(result), status_code

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
@validate_json()
def update_profile():
    """Update current user profile"""
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status_code = UserService.update_profile(user_id, data)
    return jsonify(result), status_code

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
@validate_json('current_password', 'new_password')
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status_code = UserService.change_password(
        user_id, 
        data.get('current_password'), 
        data.get('new_password')
    )
    return jsonify(result), status_code

@user_bp.route('/activities', methods=['GET'])
@jwt_required()
def get_activities():
    """Get user activities"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    from app.services.activity_service import ActivityService
    activities = ActivityService.get_user_activities(user_id, page, per_page)
    
    return jsonify({
        'activities': activities,
        'page': page,
        'per_page': per_page
    }), 200

