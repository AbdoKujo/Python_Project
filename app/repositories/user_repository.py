from app import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any

class UserRepository:
    """Repository for User model operations"""
    
    @staticmethod
    def create(user_data: Dict[str, Any]) -> Optional[User]:
        """Create a new user"""
        try:
            user = User(
                username=user_data.get('username'),
                email=user_data.get('email'),
                role=user_data.get('role', 'user')
            )
            user.password = user_data.get('password')
            
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all(page: int = 1, per_page: int = 20) -> List[User]:
        """Get all users with pagination"""
        return User.query.paginate(page=page, per_page=per_page, error_out=False).items
    
    @staticmethod
    def update(user: User, user_data: Dict[str, Any]) -> Optional[User]:
        """Update user data"""
        try:
            for key, value in user_data.items():
                if key == 'password':
                    user.password = value
                elif hasattr(user, key):
                    setattr(user, key, value)
            
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(user: User) -> bool:
        """Delete a user"""
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_last_login(user: User) -> Optional[User]:
        """Update user's last login timestamp"""
        from datetime import datetime
        try:
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

