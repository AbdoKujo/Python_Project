from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps
from app.repositories.user_repository import UserRepository
import jwt

def register_routes(app):
    """Register all application routes"""
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return {'status': 'ok'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        # Check if request is for API
        if request.path.startswith('/auth/') or request.path.startswith('/user/') or \
           request.path.startswith('/admin/') or request.path.startswith('/activity/'):
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 errors"""
        # Check if request is for API
        if request.path.startswith('/auth/') or request.path.startswith('/user/') or \
           request.path.startswith('/admin/') or request.path.startswith('/activity/'):
        # Ensure we return a JSON response for API routes
            return jsonify({'error': str(error) or 'Bad Request'}), 400
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        current_app.logger.error('Server Error: %s', error)
        # Check if request is for API
        if request.path.startswith('/auth/') or request.path.startswith('/user/') or \
           request.path.startswith('/admin/') or request.path.startswith('/activity/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500
    
    # Authentication middleware for pages that checks both cookie and localStorage
    def auth_required_page(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check for token in request cookies (server-side auth)
            token = request.cookies.get('access_token')
            
            if not token:
                # If no token in cookies, the client-side JS will handle auth
                # We'll render the page and let JS redirect if needed
                pass
            else:
                # Verify the token from cookies
                try:
                    # Manually decode the token to avoid exceptions
                    jwt_secret = app.config['JWT_SECRET_KEY']
                    decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
                    user_id = decoded.get('sub')
                    
                    # Set user in session for template access
                    user = UserRepository.get_by_id(user_id)
                    if user:
                        session['user_id'] = user_id
                        session['user_role'] = user.role
                except Exception as e:
                    current_app.logger.error(f"Token verification error: {str(e)}")
                    # Token is invalid, but we'll let client-side handle it
                    pass
            
            return f(*args, **kwargs)
        return decorated_function
    
    # Admin middleware for pages
    def admin_required_page(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check for token in request cookies (server-side auth)
            token = request.cookies.get('access_token')
            
            if not token:
                # If no token in cookies, the client-side JS will handle auth
                # We'll render the page and let JS redirect if needed
                pass
            else:
                # Verify the token from cookies
                try:
                    # Manually decode the token to avoid exceptions
                    jwt_secret = app.config['JWT_SECRET_KEY']
                    decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
                    user_id = decoded.get('sub')
                    user_role = decoded.get('role')
                    
                    # Set user in session for template access
                    if user_role != 'admin':
                        flash('Admin access required', 'error')
                        return redirect(url_for('main.index'))
                    
                    session['user_id'] = user_id
                    session['user_role'] = user_role
                except Exception as e:
                    current_app.logger.error(f"Token verification error: {str(e)}")
                    # Token is invalid, but we'll let client-side handle it
                    pass
            
            return f(*args, **kwargs)
        return decorated_function
    
    # Register main routes
    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)
    
    # Register auth routes
    from app.controllers.auth_controller import auth_bp
    
    # Add login and register page routes to auth blueprint
    @auth_bp.route('/login', methods=['GET'])
    def login_page():
        """Render login page"""
        return render_template('auth/login.html')
    
    @auth_bp.route('/register', methods=['GET'])
    def register_page():
        """Render register page"""
        return render_template('auth/register.html')
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Register user routes
    from app.controllers.user_controller import user_bp
    
    # Add profile page route to user blueprint
    @user_bp.route('/profile-page', methods=['GET'])
    @auth_required_page
    def user_profile_page():
        """Render user profile page"""
        return render_template('user/profile.html')
    
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Register admin routes
    from app.controllers.admin_controller import admin_bp
    
    # Add admin page routes to admin blueprint
    @admin_bp.route('/dashboard', methods=['GET'])
    @admin_required_page
    def admin_dashboard_page():
        """Render admin dashboard page"""
        return render_template('admin/dashboard.html')
    
    @admin_bp.route('/user-management', methods=['GET'])
    @admin_required_page
    def admin_user_management_page():
        """Render admin user management page"""
        return render_template('admin/user_management.html')
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register activity routes
    from app.controllers.activity_controller import activity_bp
    app.register_blueprint(activity_bp, url_prefix='/activity')

