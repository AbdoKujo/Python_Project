import secrets
import string
from typing import Dict, Any
import hashlib
import hmac
import base64
from flask import current_app

def generate_random_string(length: int = 32) -> str:
    """Generate a secure random string"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    """Hash a password (alternative to werkzeug)"""
    salt = generate_random_string(16)
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    hash_b64 = base64.b64encode(hash_obj).decode('utf-8')
    return f"{salt}${hash_b64}"

def verify_password_hash(password_hash: str, password: str) -> bool:
    """Verify a password against a hash (alternative to werkzeug)"""
    if '$' not in password_hash:
        return False
    
    salt, hash_b64 = password_hash.split('$', 1)
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    new_hash_b64 = base64.b64encode(hash_obj).decode('utf-8')
    
    return hmac.compare_digest(hash_b64, new_hash_b64)

def sanitize_input(input_str: str) -> str:
    """Sanitize input to prevent XSS"""
    # Basic sanitization - replace < and > with their HTML entities
    return input_str.replace('<', '&lt;').replace('>', '&gt;')

def generate_csrf_token() -> str:
    """Generate a CSRF token"""
    return generate_random_string(32)

def secure_headers() -> Dict[str, str]:
    """Return secure headers for HTTP responses"""
    return {
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self';",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }

