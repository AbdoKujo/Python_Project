import re
from typing import Dict, Any, List

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength"""
    # At least 8 characters, containing letters and numbers
    if len(password) < 8:
        return False
    
    # Check for at least one letter and one number
    has_letter = False
    has_number = False
    
    for char in password:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_number = True
    
    return has_letter and has_number

def validate_username(username: str) -> bool:
    """Validate username format"""
    # Alphanumeric with underscores, 3-20 characters
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))

def validate_input(data: Dict[str, Any], rules: Dict[str, List[callable]]) -> Dict[str, List[str]]:
    """Validate input data against rules"""
    errors = {}
    
    for field, validators in rules.items():
        field_errors = []
        
        # Skip if field is not in data
        if field not in data:
            continue
        
        value = data[field]
        
        # Apply each validator
        for validator in validators:
            try:
                if not validator(value):
                    # Get validator name for error message
                    validator_name = validator.__name__.replace('validate_', '')
                    field_errors.append(f"Invalid {validator_name}")
            except Exception:
                field_errors.append("Validation error")
        
        if field_errors:
            errors[field] = field_errors
    
    return errors

