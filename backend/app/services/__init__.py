"""
Services Package - Business Logic Layer (IoC Pattern)

Services contain all business logic and are injected into routes.
This separation follows the Inversion of Control principle:
- Routes depend on service abstractions, not implementations
- Services can be easily swapped or mocked for testing
- Business logic is centralized and reusable
"""
from .auth_service import AuthService
from .post_service import PostService
from .comment_service import CommentService
from .rss_service import RSSService

# Service instances (can be replaced for testing)
auth_service = AuthService()
post_service = PostService()
comment_service = CommentService()
rss_service = RSSService()

__all__ = [
    'AuthService', 'PostService', 'CommentService', 'RSSService',
    'auth_service', 'post_service', 'comment_service', 'rss_service'
]
