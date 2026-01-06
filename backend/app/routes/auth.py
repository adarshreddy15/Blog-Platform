"""
Authentication Routes - User and Admin registration and login
"""
from flask import Blueprint, request, jsonify
from ..services import auth_service

auth_bp = Blueprint('auth', __name__)


# ============ User Registration & Login ============

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """
    Register a new regular user.

    Request body:
    {
        "email": "user@example.com",
        "username": "user",
        "password": "password123"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['email', 'username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    user, error = auth_service.register_user(
        email=data['email'],
        username=data['username'],
        password=data['password']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'User registered successfully',
        'user': user
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login_user():
    """
    Login as user and receive JWT token.

    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    result, error = auth_service.login_user(
        email=data['email'],
        password=data['password']
    )

    if error:
        return jsonify({'error': error}), 401

    return jsonify({
        'message': 'Login successful',
        **result
    }), 200


# ============ Admin Registration & Login ============

@auth_bp.route('/admin/register', methods=['POST'])
def register_admin():
    """
    Register a new admin user with special admin code.

    Request body:
    {
        "email": "admin@example.com",
        "username": "admin",
        "password": "password123",
        "admin_code": "your-secret-admin-code"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['email', 'username', 'password', 'admin_code']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    user, error = auth_service.register_admin(
        email=data['email'],
        username=data['username'],
        password=data['password'],
        admin_code=data['admin_code']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Admin registered successfully',
        'user': user
    }), 201


@auth_bp.route('/admin/login', methods=['POST'])
def login_admin():
    """
    Login as admin and receive JWT token.

    Request body:
    {
        "email": "admin@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    result, error = auth_service.login_admin(
        email=data['email'],
        password=data['password']
    )

    if error:
        return jsonify({'error': error}), 401

    return jsonify({
        'message': 'Admin login successful',
        **result
    }), 200

