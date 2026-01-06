from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import comment_service

# ✅ DEFINE BLUEPRINT FIRST
comments_bp = Blueprint('comments', __name__)

# ---------------- PUBLIC ROUTES ---------------- #

@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = comment_service.get_approved_comments(post_id)
    return jsonify({'comments': comments}), 200


@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['guest_name', 'guest_email', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    comment, error = comment_service.create_comment(
        post_id=post_id,
        guest_name=data['guest_name'],
        guest_email=data['guest_email'],
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Comment submitted successfully. It will appear after approval.',
        'comment': comment
    }), 201


# ---------------- USER ROUTES (🔥 YOUR MISSING PART) ---------------- #

@comments_bp.route('/comments/my', methods=['GET'])
@jwt_required()
def get_my_comments():
    user_id = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    data = comment_service.get_user_comments(
        user_id=user_id,
        page=page,
        per_page=per_page
    )

    return jsonify(data), 200
# ---------------- USER CREATE COMMENT ---------------- #

@comments_bp.route('/user/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_user_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    comment, error = comment_service.create_user_comment(
        post_id=post_id,
        user_id=user_id,
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Comment added successfully',
        'comment': comment
    }), 201


@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_my_comment(comment_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    comment, error = comment_service.update_user_comment(
        comment_id=comment_id,
        user_id=user_id,
        content=data['content']
    )

    if error:
        return jsonify({'error': error}), 403

    return jsonify({'comment': comment}), 200


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_my_comment(comment_id):
    user_id = get_jwt_identity()

    success, error = comment_service.delete_user_comment(
        comment_id=comment_id,
        user_id=user_id
    )

    if error:
        return jsonify({'error': error}), 403

    return jsonify({'message': 'Comment deleted successfully'}), 200
