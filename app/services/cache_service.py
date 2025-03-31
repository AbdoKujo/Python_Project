from app import cache
from typing import Any, Optional
from datetime import timedelta

class CacheService:
    """Service for cache operations"""
    
    @staticmethod
    def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """Set a cache value"""
        return cache.set(key, value, timeout=timeout)
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a cache value"""
        value = cache.get(key)
        return value if value is not None else default
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete a cache value"""
        return cache.delete(key)
    
    @staticmethod
    def clear() -> bool:
        """Clear all cache"""
        return cache.clear()
    
    @staticmethod
    def has(key: str) -> bool:
        """Check if cache has a key"""
        return cache.has(key)
    
    @staticmethod
    def memoize(timeout: Optional[int] = None):
        """Decorator to memoize a function"""
        return cache.memoize(timeout=timeout)
    
    @staticmethod
    def cached(timeout: Optional[int] = None, key_prefix: str = 'view'):
        """Decorator to cache a view function"""
        return cache.cached(timeout=timeout, key_prefix=key_prefix)

