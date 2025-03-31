from app import db, create_app
from app.models.user import User
from werkzeug.security import generate_password_hash
import os

def seed_database():
    """Seed the database with initial data"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Seed admin user
        seed_admin_user()
        
        # Seed test users
        seed_test_users()

def seed_admin_user():
    """Seed an admin user"""
    # Check if admin user already exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print("Admin user already exists")
        return
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin',
        is_active=True,
        is_deleted=False  # Explicitly set is_deleted
    )
    admin.password = 'Admin123!'
    
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully")

def seed_test_users():
    """Seed test users"""
    # Create test users
    users = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'User123!',
            'role': 'user',
            'is_deleted': False
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'User123!',
            'role': 'user',
            'is_deleted': False
        }
    ]
    
    for user_data in users:
        # Check if user already exists
        user = User.query.filter_by(username=user_data['username']).first()
        if user:
            print(f"User {user_data['username']} already exists")
            continue
        
        # Create user
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            role=user_data['role'],
            is_active=True,
            is_deleted=user_data['is_deleted']
        )
        user.password = user_data['password']
        
        db.session.add(user)
    
    db.session.commit()
    print("Test users created successfully")

if __name__ == '__main__':
    # Use a single app context for all seeding operations
    seed_database()

