from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('user/home.html')

@main_bp.route('/login')
def login():
    """Redirect to login page"""
    return redirect(url_for('auth.login_page'))

@main_bp.route('/register')
def register():
    """Redirect to register page"""
    return redirect(url_for('auth.register_page'))

