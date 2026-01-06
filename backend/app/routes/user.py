"""
User Routes - Protected endpoints for regular users to manage their own content
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from ..services import post_service, comment_service
from ..utils import user_required, get_current_user

user_bp = Blueprint('user', __name__)


# ============ User Dashboard ============

@user_bp.route('/dashboard', methods=['GET'])
@user_required
def get_dashboard():
    """Get user dashboard with their stats"""
    user_id = get_jwt_identity()
    user = get_current_user()

    # Get user's post count
    from ..models import Post, Comment
    user_posts = Post.query.filter_by(author_id=user_id).count()
    user_comments = Comment.query.filter_by(author_id=user_id).count()

    return jsonify({
        'user': user.to_dict() if user else None,
        'stats': {
            'total_posts': user_posts,
            'total_comments': user_comments
        }
    }), 200


# ============ User Posts Management ============

@user_bp.route('/posts', methods=['GET'])
@user_required
def get_user_posts():
    """Get all posts created by the current user"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    status = request.args.get('status')

    user_id = int(get_jwt_identity())

    result = post_service.get_user_posts(
        user_id=user_id,
        page=page,
        per_page=per_page,
        status=status
    )
    return jsonify(result), 200


@user_bp.route('/posts/<int:post_id>', methods=['GET'])
@user_required
def get_user_post(post_id):
    """Get a specific post owned by the user"""
    user_id = int(get_jwt_identity())

    post = post_service.get_post_by_id(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Check if post belongs to user
    if post.get('author_id') != user_id:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify(post), 200


@user_bp.route('/posts', methods=['POST'])
@user_required
def create_user_post():
    """
    Create a new blog post.

    Request body:
    {
        "title": "Post Title",
        "content": "<p>HTML content...</p>",
        "excerpt": "Short description",
        "tags": ["tag1", "tag2"],
        "status": "draft" or "published",
        "featured_image": "/uploads/posts/image.jpg"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    user_id = get_jwt_identity()

    post, error = post_service.create_post(
        title=data['title'],
        content=data['content'],
        author_id=user_id,
        excerpt=data.get('excerpt'),
        tags=data.get('tags', []),
        featured_image=data.get('featured_image'),
        status=data.get('status', 'draft')
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Post created successfully',
        'post': post
    }), 201


@user_bp.route('/posts/<int:post_id>', methods=['PUT'])
@user_required
def update_user_post(post_id):
    """Update a post owned by the user"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user_id = int(get_jwt_identity())

    # Check ownership before update
    existing_post = post_service.get_post_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404

    if existing_post.get('author_id') != user_id:
        return jsonify({'error': 'Access denied'}), 403

    post, error = post_service.update_post(post_id, **data)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Post updated successfully',
        'post': post
    }), 200


@user_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@user_required
def delete_user_post(post_id):
    """Delete a post owned by the user"""
    user_id = int(get_jwt_identity())
    
    # Check ownership before delete
    existing_post = post_service.get_post_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404

    if existing_post.get('author_id') != user_id:
        return jsonify({'error': f'Access denied. Post author is {existing_post.get("author_id")}, current user is {user_id}'}), 403

    success, error = post_service.delete_post(post_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Post deleted successfully'}), 200


@user_bp.route('/posts/upload', methods=['POST'])
@user_required
def upload_user_image():
    """
    Upload an image for a blog post.
    Returns the image URL to be used in the post.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    result, error = post_service.upload_image(file)

    if error:
        return jsonify({'error': error}), 400

    return jsonify(result), 200


# ============ User Comments Management ============

@user_bp.route('/comments', methods=['GET'])
@user_required
def get_user_comments():
    """Get all comments created by the current user"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    user_id = get_jwt_identity()

    result = comment_service.get_user_comments(
        user_id=user_id,
        page=page,
        per_page=per_page
    )
    return jsonify(result), 200


@user_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@user_required
def create_user_comment(post_id):
    """
    Create a comment as an authenticated user.

    Request body:
    {
        "content": "Comment text"
    }
    """
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    user_id = get_jwt_identity()

    comment, error = comment_service.create_user_comment(
        post_id=post_id,
        user_id=user_id,
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Comment created successfully',
        'comment': comment
    }), 201


@user_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@user_required
def update_user_comment(comment_id):
    """Update a comment owned by the user"""
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    user_id = get_jwt_identity()

    comment, error = comment_service.update_user_comment(
        comment_id=comment_id,
        user_id=user_id,
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Comment updated successfully',
        'comment': comment
    }), 200


@user_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@user_required
def delete_user_comment(comment_id):
    """Delete a comment owned by the user"""
    user_id = get_jwt_identity()

    success, error = comment_service.delete_user_comment(
        comment_id=comment_id,
        user_id=user_id
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Comment deleted successfully'}), 200
