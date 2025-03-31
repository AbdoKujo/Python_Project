from app.repositories.activity_repository import ActivityRepository
from flask import Request
from typing import Dict, Any, List, Optional

class ActivityService:
    """Service for activity tracking operations"""
    
    @staticmethod
    def log_activity(user_id: int, action: str, details: Optional[str] = None, 
                    request: Optional[Request] = None) -> Dict[str, Any]:
        """Log a user activity"""
        activity_data = {
            'user_id': user_id,
            'action': action,
            'details': details
        }
        
        # Add request information if available
        if request:
            activity_data['ip_address'] = request.remote_addr
            activity_data['user_agent'] = request.user_agent.string
        
        try:
            activity = ActivityRepository.create(activity_data)
            return {
                'id': activity.id,
                'user_id': activity.user_id,
                'action': activity.action,
                'timestamp': activity.timestamp.isoformat()
            }
        except Exception as e:
            # Log the error but don't fail the main operation
            print(f"Error logging activity: {str(e)}")
            return {}
    
    @staticmethod
    def get_user_activities(user_id: int, page: int = 1, per_page: int = 20) -> List[Dict[str, Any]]:
        """Get activities for a user"""
        activities = ActivityRepository.get_by_user_id(user_id, page, per_page)
        return [
            {
                'id': activity.id,
                'action': activity.action,
                'details': activity.details,
                'ip_address': activity.ip_address,
                'user_agent': activity.user_agent,
                'timestamp': activity.timestamp.isoformat()
            }
            for activity in activities
        ]
    
    @staticmethod
    def get_all_activities(page: int = 1, per_page: int = 20) -> List[Dict[str, Any]]:
        """Get all activities"""
        activities = ActivityRepository.get_all(page, per_page)
        return [
            {
                'id': activity.id,
                'user_id': activity.user_id,
                'action': activity.action,
                'details': activity.details,
                'ip_address': activity.ip_address,
                'user_agent': activity.user_agent,
                'timestamp': activity.timestamp.isoformat()
            }
            for activity in activities
        ]

