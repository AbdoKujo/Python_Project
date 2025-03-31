from app.repositories.user_repository import UserRepository
from app.services.activity_service import ActivityService
from app.utils.validators import validate_email, validate_password
from typing import Dict, Any, Tuple, List
from flask import request

class UserService:
    """Service for user operations"""
    
    @staticmethod
    def get_profile(user_id: int) -> Tuple[Dict[str, Any], int]:
        """Get user profile"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        }, 200
    
    @staticmethod
    def update_profile(user_id: int, user_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Update user profile"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate email if provided
        if 'email' in user_data and not validate_email(user_data.get('email', '')):
            return {'error': 'Invalid email format'}, 400
        
        # Remove sensitive fields that shouldn't be updated directly
        safe_data = {k: v for k, v in user_data.items() if k in ['username', 'email']}
        
        try:
            updated_user = UserRepository.update(user, safe_data)
            
            # Log activity
            ActivityService.log_activity(
                user_id=user_id,
                action='profile_updated',
                details='User profile updated',
                request=request
            )
            
            return {
                'message': 'Profile updated successfully',
                'user': {
                    'id': updated_user.id,
                    'username': updated_user.username,
                    'email': updated_user.email
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> Tuple[Dict[str, Any], int]:
        """Change user password"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Verify current password
        if not user.verify_password(current_password):
            return {'error': 'Current password is incorrect'}, 401
        
        # Validate new password
        if not validate_password(new_password):
            return {'error': 'Password must be at least 8 characters and contain letters and numbers'}, 400
        
        try:
            # Update password
            UserRepository.update(user, {'password': new_password})
            
            # Log activity
            ActivityService.log_activity(
                user_id=user_id,
                action='password_changed',
                details='User password changed',
                request=request
            )
            
            return {'message': 'Password changed successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 20) -> Tuple[Dict[str, Any], int]:
        """Get all users (admin only)"""
        users = UserRepository.get_all(page, per_page)
        
        return {
            'users': [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'is_active': user.is_active,
                    'created_at': user.created_at.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None
                }
                for user in users
            ],
            'page': page,
            'per_page': per_page
        }, 200
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Tuple[Dict[str, Any], int]:
        """Get user by ID (admin only)"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        }, 200
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Create a new user (admin only)"""
        # Validate input
        if not validate_email(user_data.get('email', '')):
            return {'error': 'Invalid email format'}, 400
        
        if not validate_password(user_data.get('password', '')):
            return {'error': 'Password must be at least 8 characters and contain letters and numbers'}, 400
        
        # Check if user already exists
        if UserRepository.get_by_email(user_data.get('email')):
            return {'error': 'Email already registered'}, 409
        
        if UserRepository.get_by_username(user_data.get('username')):
            return {'error': 'Username already taken'}, 409
        
        # Create user
        try:
            user = UserRepository.create(user_data)
            
            # Log activity
            ActivityService.log_activity(
                user_id=user.id,
                action='user_created',
                details=f'User created by admin',
                request=request
            )
            
            return {
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def update_user(user_id: int, user_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Update a user (admin only)"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate email if provided
        if 'email' in user_data and not validate_email(user_data.get('email', '')):
            return {'error': 'Invalid email format'}, 400
        
        # Validate password if provided
        if 'password' in user_data and not validate_password(user_data.get('password', '')):
            return {'error': 'Password must be at least 8 characters and contain letters and numbers'}, 400
        
        try:
            updated_user = UserRepository.update(user, user_data)
            
            # Log activity
            action = 'user_updated'
            details = 'User updated by admin'
            
            if 'is_active' in user_data:
                if user_data['is_active']:
                    action = 'user_activated'
                    details = 'User activated by admin'
                else:
                    action = 'user_deactivated'
                    details = 'User deactivated by admin'
            
            ActivityService.log_activity(
                user_id=user_id,
                action=action,
                details=details,
                request=request
            )
            
            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'username': updated_user.username,
                    'email': updated_user.email,
                    'role': updated_user.role,
                    'is_active': updated_user.is_active
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def delete_user(user_id: int) -> Tuple[Dict[str, Any], int]:
        """Delete a user (admin only)"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            # Log activity before deletion
            ActivityService.log_activity(
                user_id=user_id,
                action='user_deleted',
                details='User deleted by admin',
                request=request
            )
            
            # Perform soft delete if the model supports it
            if hasattr(user, 'is_deleted'):
                UserRepository.update(user, {'is_deleted': True, 'is_active': False})
                return {'message': 'User deleted successfully'}, 200
            
            # Otherwise perform hard delete
            UserRepository.delete(user)
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

