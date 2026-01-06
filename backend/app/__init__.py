"""
Flask Application Factory - IoC Pattern Implementation
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

from .extensions import db, jwt, migrate
from .config import Config


def create_app(config_class=Config):
    """
    Application factory pattern (IoC)
    """
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ DEBUG: confirm DB URL
    print("✅ DB URL:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # ---------------- JWT CONFIG ---------------- #

    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return user_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from .models.user import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    # ---------------- CORS CONFIG ---------------- #

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/uploads/*": {
            "origins": "*"
        }
    })

    # ---------------- REGISTER BLUEPRINTS ---------------- #

    from .routes import auth_bp, posts_bp, comments_bp, admin_bp, rss_bp, user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(posts_bp, url_prefix="/api/posts")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(rss_bp, url_prefix="/api")
    

    # ---------------- 🔥 IMPORT MODELS (CRITICAL) ---------------- #
    # SQLAlchemy will NOT create tables if models are not imported

    from .models.user import User
    from .models.post import Post
    from .models.comment import Comment
    # add more models here if you have them

    # ---------------- CREATE DATABASE TABLES ---------------- #

    with app.app_context():
        db.create_all()
        print("✅ PostgreSQL tables created successfully")

    # ---------------- ROUTES ---------------- #

    @app.route("/")
    def index():
        return """
        <h1>🚀 Blog Platform API</h1>
        <p>Backend is running successfully.</p>
        <ul>
            <li><a href="/api/health">Health Check</a></li>
            <li><a href="/api/posts">Posts API</a></li>
            <li><a href="/api/rss">RSS Feed</a></li>
        </ul>
        """

    @app.route("/api/health")
    def health_check():
        return {"status": "healthy", "message": "Blog API is running"}

    @app.route("/uploads/<path:filename>")
    def serve_uploads(filename):
        upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
        return send_from_directory(upload_folder, filename)

    return app
