"""
Public Posts Routes - Read-only endpoints for blog posts
"""
from flask import Blueprint, request, jsonify
from ..services import post_service

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    Get published blog posts with pagination.
    
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 50)
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    
    result = post_service.get_published_posts(page=page, per_page=per_page)
    return jsonify(result), 200


@posts_bp.route('/<slug>', methods=['GET'])
def get_post(slug):
    """Get a single published post by slug (or draft if author)"""
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    
    # Check if user is logged in (optional)
    current_user_id = None
    try:
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        if current_user_id:
            current_user_id = int(current_user_id)
    except:
        pass

    # First try to get published post
    post = post_service.get_post_by_slug(slug, published_only=True)
    
    # If not found or draft, check if current user is the author
    if not post:
        post_obj = post_service.get_post_by_slug(slug, published_only=False)
        if post_obj and current_user_id and post_obj.get('author_id') == current_user_id:
            post = post_obj
        else:
            return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(post), 200


@posts_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags with post counts"""
    tags = post_service.get_all_tags()
    return jsonify({'tags': tags}), 200


@posts_bp.route('/tags/<tag_slug>', methods=['GET'])
def get_posts_by_tag(tag_slug):
    """
    Get published posts filtered by tag.
    
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    
    result = post_service.get_posts_by_tag(tag_slug, page=page, per_page=per_page)
    
    if not result['tag']:
        return jsonify({'error': 'Tag not found'}), 404
    
    return jsonify(result), 200
