from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import jwt
from flask import current_app

class TokenService:
    """Service for JWT token operations"""
    
    @staticmethod
    def generate_access_token(user_id: int, role: str) -> str:
        """Generate JWT access token"""
        return create_access_token(
            identity=user_id,
            additional_claims={'role': role}
        )
    
    @staticmethod
    def generate_refresh_token(user_id: int) -> str:
        """Generate JWT refresh token"""
        return create_refresh_token(identity=user_id)
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT access token"""
        try:
            return decode_token(token)
        except Exception:
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT refresh token"""
        try:
            return decode_token(token)
        except Exception:
            return None
    
    @staticmethod
    def is_token_expired(token_data: Dict[str, Any]) -> bool:
        """Check if token is expired"""
        exp = token_data.get('exp')
        if not exp:
            return True
        
        now = datetime.now(timezone.utc).timestamp()
        return now > exp

