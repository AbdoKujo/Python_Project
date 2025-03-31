from app.repositories.user_repository import UserRepository
from typing import Dict, Any, List, Optional

class AuthorizationService:
    """Service for authorization operations"""
    
    # Define permission constants
    PERMISSIONS = {
        'user': [
            'profile:read',
            'profile:update',
            'activity:read_own'
        ],
        'admin': [
            'profile:read',
            'profile:update',
            'profile:read_any',
            'profile:update_any',
            'profile:delete_any',
            'activity:read_own',
            'activity:read_any',
            'user:create',
            'user:read',
            'user:update',
            'user:delete'
        ]
    }
    
    @staticmethod
    def get_permissions(role: str) -> List[str]:
        """Get permissions for a role"""
        return AuthorizationService.PERMISSIONS.get(role, [])
    
    @staticmethod
    def has_permission(user_id: int, permission: str) -> bool:
        """Check if user has a specific permission"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False
        
        user_permissions = AuthorizationService.get_permissions(user.role)
        return permission in user_permissions
    
    @staticmethod
    def can_access_resource(user_id: int, resource_owner_id: int, permission: str) -> bool:
        """Check if user can access a specific resource"""
        # If user is the resource owner, check for own permission
        if user_id == resource_owner_id:
            return True
        
        # Otherwise, check for any permission
        return AuthorizationService.has_permission(user_id, permission)

