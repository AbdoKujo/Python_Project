from flask import session
from typing import Any, Optional
from datetime import datetime, timedelta

class SessionService:
    """Service for session management"""
    
    @staticmethod
    def set(key: str, value: Any, expiry: Optional[timedelta] = None) -> None:
        """Set a session value"""
        session[key] = value
        
        # Set expiry if provided
        if expiry:
            session[f"{key}_exp"] = (datetime.utcnow() + expiry).timestamp()
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a session value"""
        # Check expiry if it exists
        expiry_key = f"{key}_exp"
        if expiry_key in session:
            expiry = session[expiry_key]
            if datetime.utcnow().timestamp() > expiry:
                # Expired, remove and return default
                SessionService.remove(key)
                return default
        
        return session.get(key, default)
    
    @staticmethod
    def remove(key: str) -> None:
        """Remove a session value"""
        if key in session:
            session.pop(key)
        
        # Remove expiry if it exists
        expiry_key = f"{key}_exp"
        if expiry_key in session:
            session.pop(expiry_key)
    
    @staticmethod
    def clear() -> None:
        """Clear all session data"""
        session.clear()
    
    @staticmethod
    def has(key: str) -> bool:
        """Check if session has a key"""
        return key in session

