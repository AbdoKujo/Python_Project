from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
sess = Session()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    storage_options={}
)
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    sess.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    
    # Register context processors
    from app.context_processors import user_context_processor
    app.context_processor(user_context_processor)
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask application startup')
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    # Exempt API routes from CSRF protection
    csrf.exempt('auth')
    csrf.exempt('user')
    csrf.exempt('admin')
    csrf.exempt('activity')
    
    return app

