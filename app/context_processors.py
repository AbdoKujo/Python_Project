from flask import g, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.repositories.user_repository import UserRepository
from jwt.exceptions import InvalidTokenError

def user_context_processor():
    """Add current_user to template context"""
    current_user = {
        'is_authenticated': False,
        'is_admin': False
    }
    
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        
        if user_id:
            user = UserRepository.get_by_id(user_id)
            if user:
                current_user = {
                    'is_authenticated': True,
                    'is_admin': user.is_admin(),
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
    except InvalidTokenError:
        # Invalid token, just continue with unauthenticated user
        pass
    except Exception as e:
        # Log the error but continue
        print(f"Error in user_context_processor: {str(e)}")
    
    return {'current_user': current_user}

