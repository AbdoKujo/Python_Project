from flask import Blueprint, request, jsonify
from app.services.activity_service import ActivityService
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required()
def get_all_activities():
    """Get all activities (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    activities = ActivityService.get_all_activities(page, per_page)
    
    return jsonify({
        'activities': activities,
        'page': page,
        'per_page': per_page
    }), 200

@activity_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_user_activities(user_id):
    """Get activities for a specific user (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    activities = ActivityService.get_user_activities(user_id, page, per_page)
    
    return jsonify({
        'activities': activities,
        'user_id': user_id,
        'page': page,
        'per_page': per_page
    }), 200

