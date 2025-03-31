from app import db
from app.models.activity import Activity
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any

class ActivityRepository:
    """Repository for Activity model operations"""
    
    @staticmethod
    def create(activity_data: Dict[str, Any]) -> Optional[Activity]:
        """Create a new activity record"""
        try:
            activity = Activity(
                user_id=activity_data.get('user_id'),
                action=activity_data.get('action'),
                details=activity_data.get('details'),
                ip_address=activity_data.get('ip_address'),
                user_agent=activity_data.get('user_agent')
            )
            
            db.session.add(activity)
            db.session.commit()
            return activity
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_by_id(activity_id: int) -> Optional[Activity]:
        """Get activity by ID"""
        return Activity.query.get(activity_id)
    
    @staticmethod
    def get_by_user_id(user_id: int, page: int = 1, per_page: int = 20) -> List[Activity]:
        """Get activities by user ID with pagination"""
        return Activity.query.filter_by(user_id=user_id).order_by(
            Activity.timestamp.desc()
        ).paginate(page=page, per_page=per_page, error_out=False).items
    
    @staticmethod
    def get_all(page: int = 1, per_page: int = 20) -> List[Activity]:
        """Get all activities with pagination"""
        return Activity.query.order_by(
            Activity.timestamp.desc()
        ).paginate(page=page, per_page=per_page, error_out=False).items
    
    @staticmethod
    def delete(activity: Activity) -> bool:
        """Delete an activity"""
        try:
            db.session.delete(activity)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_by_user_id(user_id: int) -> bool:
        """Delete all activities for a user"""
        try:
            Activity.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

