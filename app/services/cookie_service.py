from flask import request, make_response, Response
from typing import Any, Optional
from datetime import datetime, timedelta

class CookieService:
    """Service for cookie operations"""
    
    @staticmethod
    def set(response: Response, key: str, value: str, max_age: Optional[int] = None, 
            expires: Optional[datetime] = None, path: str = '/', domain: Optional[str] = None, 
            secure: bool = False, httponly: bool = False, samesite: Optional[str] = None) -> Response:
        """Set a cookie"""
        response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite
        )
        return response
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a cookie value"""
        return request.cookies.get(key, default)
    
    @staticmethod
    def delete(response: Response, key: str, path: str = '/', domain: Optional[str] = None) -> Response:
        """Delete a cookie"""
        response.delete_cookie(key, path=path, domain=domain)
        return response
    
    @staticmethod
    def has(key: str) -> bool:
        """Check if request has a cookie"""
        return key in request.cookies

