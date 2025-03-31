from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService
from app.services.activity_service import ActivityService
from app.utils.validators import validate_email, validate_password
from typing import Dict, Any, Optional, Tuple
from flask import request

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register(user_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Register a new user"""
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
                action='user_registered',
                details='User registered successfully',
                request=request
            )
            
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def login(credentials: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Login a user"""
        username = credentials.get('username')
        password = credentials.get('password')
        
        # Find user by username or email
        user = UserRepository.get_by_username(username)
        if not user:
            user = UserRepository.get_by_email(username)
        
        # Verify user and password
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        # Check if user has been deleted (soft delete implementation)
        if hasattr(user, 'is_deleted') and user.is_deleted:
            return {'error': 'Your account has been deleted. Please contact support for assistance.'}, 403
        
        # Check if user is active
        if not user.is_active:
            return {'error': 'Your account has been deactivated. Please contact support for assistance.'}, 403
        
        # Verify password
        if not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # Update last login
        UserRepository.update_last_login(user)
        
        # Generate tokens
        access_token = TokenService.generate_access_token(user.id, user.role)
        refresh_token = TokenService.generate_refresh_token(user.id)
        
        # Log activity
        ActivityService.log_activity(
            user_id=user.id,
            action='user_login',
            details='User logged in successfully',
            request=request
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }, 200
    
    @staticmethod
    def logout(user_id: int) -> Tuple[Dict[str, Any], int]:
        """Logout a user"""
        # Log activity
        ActivityService.log_activity(
            user_id=user_id,
            action='user_logout',
            details='User logged out successfully',
            request=request
        )
        
        # In a real application, you might want to invalidate the token
        # This would require a token blacklist implementation
        
        return {'message': 'Logged out successfully'}, 200
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Tuple[Dict[str, Any], int]:
        """Refresh access token"""
        try:
            # Verify refresh token
            token_data = TokenService.verify_refresh_token(refresh_token)
            if not token_data:
                return {'error': 'Invalid refresh token'}, 401
            
            user_id = token_data.get('sub')
            
            # Get user
            user = UserRepository.get_by_id(user_id)
            
            # Check if user exists and is active
            if not user:
                return {'error': 'User not found'}, 401
                
            if hasattr(user, 'is_deleted') and user.is_deleted:
                return {'error': 'Your account has been deleted. Please contact support for assistance.'}, 403
                
            if not user.is_active:
                return {'error': 'Your account has been deactivated. Please contact support for assistance.'}, 403
            
            # Generate new access token
            new_access_token = TokenService.generate_access_token(user.id, user.role)
            
            return {'access_token': new_access_token}, 200
        except Exception as e:
            return {'error': str(e)}, 401

