"""
Flask Extensions - Centralized extension management for IoC
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize extensions without app (IoC pattern)
# These will be configured in the app factory
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
