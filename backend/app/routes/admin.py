"""
Admin Routes - Protected endpoints for content management
"""

from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import get_jwt_identity

from ..services import post_service, comment_service, auth_service
from ..utils import admin_required

admin_bp = Blueprint('admin', __name__)

# ======================================================
# DASHBOARD
# ======================================================

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    posts_data = post_service.get_all_posts(page=1, per_page=1)
    pending_comments = comment_service.get_pending_count()
    users_data = auth_service.get_all_users(page=1, per_page=1)

    admin_id = get_jwt_identity()
    admin_user = auth_service.get_user_by_id(admin_id)

    return jsonify({
        'user': admin_user.to_dict(),
        'stats': {
            'total_posts': posts_data['total'],
            'pending_comments': pending_comments,
            'total_users': users_data['total']
        }
    }), 200


# ======================================================
# POSTS MANAGEMENT
# ======================================================

@admin_bp.route('/posts', methods=['GET'])
@admin_required
def admin_get_all_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    status = request.args.get('status')

    result = post_service.get_all_posts(page, per_page, status)
    return jsonify(result), 200


@admin_bp.route('/posts/<int:post_id>', methods=['GET'])
@admin_required
def admin_get_post(post_id):
    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post), 200


@admin_bp.route('/posts', methods=['POST'])
@admin_required
def admin_create_post():
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    author_id = get_jwt_identity()

    post, error = post_service.create_post(
        title=data['title'],
        content=data['content'],
        author_id=author_id,
        excerpt=data.get('excerpt'),
        tags=data.get('tags', []),
        featured_image=data.get('featured_image'),
        status=data.get('status', 'draft')
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Post created', 'post': post}), 201


@admin_bp.route('/posts/<int:post_id>', methods=['PUT'])
@admin_required
def admin_update_post(post_id):
    data = request.get_json()

    post, error = post_service.update_post(post_id, **data)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Post updated', 'post': post}), 200


@admin_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@admin_required
def admin_delete_post(post_id):
    success, error = post_service.delete_post(post_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Post deleted'}), 200


# ======================================================
# COMMENTS MANAGEMENT (🔥 FULL ADMIN POWER)
# ======================================================

@admin_bp.route('/comments', methods=['GET'])
@admin_required
def admin_get_all_comments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    status = request.args.get('status')

    result = comment_service.get_all_comments(page, per_page, status)
    return jsonify(result), 200


# ✏️ EDIT COMMENT CONTENT
@admin_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@admin_required
def admin_update_comment(comment_id):
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    comment, error = comment_service.admin_update_comment(
        comment_id=comment_id,
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Comment updated successfully',
        'comment': comment
    }), 200


# ✅ APPROVE / ❌ REJECT COMMENT
@admin_bp.route('/comments/<int:comment_id>/moderate', methods=['PUT'])
@admin_required
def admin_moderate_comment(comment_id):
    data = request.get_json()

    if not data or 'action' not in data:
        return jsonify({'error': 'Action is required'}), 400

    comment, error = comment_service.moderate_comment(
        comment_id=comment_id,
        action=data['action']   # approve | reject
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': f'Comment {data["action"]}d successfully',
        'comment': comment
    }), 200


# 🗑 DELETE COMMENT
@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def admin_delete_comment(comment_id):
    success, error = comment_service.delete_comment(comment_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Comment deleted'}), 200


# ======================================================
# USER MANAGEMENT
# ======================================================

@admin_bp.route('/users', methods=['GET'])
@admin_required
def admin_get_all_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    return jsonify(auth_service.get_all_users(page, per_page)), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    admin_id = get_jwt_identity()

    if admin_id == user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400

    success, error = auth_service.delete_user(user_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'User deleted'}), 200


# ======================================================
# STATIC FILES
# ======================================================

@admin_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)
