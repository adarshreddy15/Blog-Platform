"""
Routes Package - API Endpoints
"""
from .auth import auth_bp
from .posts import posts_bp
from .comments import comments_bp
from .admin import admin_bp
from .rss import rss_bp
from .user import user_bp

__all__ = ['auth_bp', 'posts_bp', 'comments_bp', 'admin_bp', 'rss_bp', 'user_bp']
