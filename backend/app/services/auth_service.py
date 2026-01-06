"""
Authentication Service - Handle admin user registration and login
"""
from ..models import User
from ..extensions import db
from flask_jwt_extended import create_access_token
from flask import current_app


class AuthService:
    """
    Authentication service following IoC principle.
    All auth-related business logic is encapsulated here.
    """

    def register_user(self, email, username, password):
        """
        Register a new regular user.

        Args:
            email: User email
            username: Display username
            password: Plain text password (will be hashed)

        Returns:
            tuple: (user_dict, error_message)
        """
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return None, 'Email already registered'

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return None, 'Username already taken'

        # Validate password strength
        if len(password) < 6:
            return None, 'Password must be at least 6 characters'

        try:
            # Create new regular user
            user = User(
                email=email,
                username=username,
                is_admin=False
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return user.to_dict(), None

        except Exception as e:
            db.session.rollback()
            return None, f'Registration failed: {str(e)}'

    def register_admin(self, email, username, password, admin_code):
        """
        Register a new admin user with special admin code.

        Args:
            email: User email
            username: Display username
            password: Plain text password (will be hashed)
            admin_code: Required special code to create admin

        Returns:
            tuple: (user_dict, error_message)
        """
        # Check admin code
        required_code = current_app.config.get('ADMIN_REGISTRATION_CODE')
        if not required_code:
            return None, 'Admin registration is disabled'

        if admin_code != required_code:
            return None, 'Invalid admin code'

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return None, 'Email already registered'

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return None, 'Username already taken'

        # Validate password strength
        if len(password) < 6:
            return None, 'Password must be at least 6 characters'

        try:
            # Create new admin user
            user = User(
                email=email,
                username=username,
                is_admin=True
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return user.to_dict(), None

        except Exception as e:
            db.session.rollback()
            return None, f'Registration failed: {str(e)}'
    
    def login_user(self, email, password):
        """
        Authenticate any user (regular or admin) and return JWT token.

        Args:
            email: User email
            password: Plain text password

        Returns:
            tuple: (token_data, error_message)
        """
        print(f"DEBUG: Login attempt for email: {email}")
        user = User.query.filter_by(email=email).first()

        if not user:
            print(f"DEBUG: User not found for email: {email}")
            return None, 'Invalid email or password'

        print(f"DEBUG: User found: {user.username}, Checking password...")
        if not user.check_password(password):
            print(f"DEBUG: Password verification failed for user: {user.username}")
            return None, 'Invalid email or password'

        print(f"DEBUG: Login successful for user: {user.username}")

        # Create JWT token
        access_token = create_access_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, None

    def login_admin(self, email, password):
        """
        Authenticate admin user and return JWT token.

        Args:
            email: User email
            password: Plain text password

        Returns:
            tuple: (token_data, error_message)
        """
        print(f"DEBUG: Admin login attempt for email: {email}")
        user = User.query.filter_by(email=email).first()

        if not user:
            print(f"DEBUG: User not found for email: {email}")
            return None, 'Invalid email or password'

        print(f"DEBUG: User found: {user.username}, Checking password...")
        if not user.check_password(password):
            print(f"DEBUG: Password verification failed for user: {user.username}")
            return None, 'Invalid email or password'

        if not user.is_admin:
            print(f"DEBUG: User is not an admin: {user.username}")
            return None, 'Admin access required'

        print(f"DEBUG: Admin login successful for user: {user.username}")

        # Create JWT token
        access_token = create_access_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return User.query.get(user_id)

    def get_all_users(self, page=1, per_page=20):
        """
        Get all users with pagination (admin only).

        Args:
            page: Page number
            per_page: Items per page

        Returns:
            dict: Paginated user data
        """
        pagination = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }

    def delete_user(self, user_id):
        """
        Delete a user (admin only).

        Args:
            user_id: ID of user to delete

        Returns:
            tuple: (success, error_message)
        """
        user = User.query.get(user_id)

        if not user:
            return False, 'User not found'

        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete user: {str(e)}'
