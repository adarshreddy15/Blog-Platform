"""
JWT Utilities - Authentication decorators and helpers
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models import User


def admin_required(fn):
    """
    Decorator to require admin authentication for routes.
    Uses IoC principle by depending on abstraction (JWT) rather than concrete session.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            # Convert to integer if string
            if isinstance(current_user_id, str):
                current_user_id = int(current_user_id)

            # Use db.session.get for better type handling in SQLA 2.0
            from ..extensions import db
            user = db.session.get(User, current_user_id)

            if not user:
                return jsonify({'error': 'User not found'}), 404

            if not user.is_admin:
                return jsonify({'error': 'Admin access required'}), 403

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'message': str(e)}), 401

    return wrapper


def user_required(fn):
    """
    Decorator to require user authentication (both regular users and admins).
    Uses IoC principle by depending on abstraction (JWT) rather than concrete session.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            # Convert to integer if string
            if isinstance(current_user_id, str):
                current_user_id = int(current_user_id)

            # Use db.session.get for better type handling in SQLA 2.0
            from ..extensions import db
            user = db.session.get(User, current_user_id)

            if not user:
                return jsonify({'error': 'User not found'}), 404

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'message': str(e)}), 401

    return wrapper


def get_current_admin():
    """Get the current authenticated admin user"""
    try:
        current_user_id = get_jwt_identity()
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        from ..extensions import db
        return db.session.get(User, current_user_id)
    except:
        return None


def get_current_user():
    """Get the current authenticated user (admin or regular user)"""
    try:
        current_user_id = get_jwt_identity()
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        from ..extensions import db
        return db.session.get(User, current_user_id)
    except:
        return None
