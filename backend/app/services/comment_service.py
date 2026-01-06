"""
Comment Service - Guest, User commenting with Admin moderation
"""
from datetime import datetime
from ..models import Comment, Post
from ..extensions import db


class CommentService:
    """
    Comment service following IoC principle.
    Handles guest comments, user comments, and admin moderation.
    """

    # ======================================================
    # PUBLIC (GUEST)
    # ======================================================

    def get_approved_comments(self, post_id):
        """Get approved comments for a post (public view)"""
        comments = Comment.query.filter_by(
            post_id=post_id,
            status='approved'
        ).order_by(Comment.created_at.desc()).all()

        return [comment.to_dict() for comment in comments]

    def create_comment(self, post_id, guest_name, guest_email, content):
        """
        Create a new guest comment.
        Guest comments are pending until admin approval.
        """
        try:
            post = Post.query.get(post_id)
            if not post:
                return None, 'Post not found'

            if post.status != 'published':
                return None, 'Cannot comment on unpublished posts'

            if not guest_name or len(guest_name.strip()) < 2:
                return None, 'Name must be at least 2 characters'

            if not guest_email or '@' not in guest_email:
                return None, 'Valid email is required'

            if not content or len(content.strip()) < 5:
                return None, 'Comment must be at least 5 characters'

            comment = Comment(
                post_id=post_id,
                guest_name=guest_name.strip(),
                guest_email=guest_email.strip().lower(),
                content=content.strip(),
                status='pending'
            )

            db.session.add(comment)
            db.session.commit()

            return comment.to_dict(), None

        except Exception as e:
            db.session.rollback()
            return None, f'Failed to submit comment: {str(e)}'

    # ======================================================
    # USER (AUTHENTICATED)
    # ======================================================

    def create_user_comment(self, post_id, user_id, content):
        """
        Create a new comment by an authenticated user.
        User & admin comments are auto-approved.
        """
        try:
            post = Post.query.get(post_id)
            if not post:
                return None, 'Post not found'

            if post.status != 'published':
                return None, 'Cannot comment on unpublished posts'

            if not content or len(content.strip()) < 5:
                return None, 'Comment must be at least 5 characters'

            comment = Comment(
                post_id=post_id,
                author_id=user_id,
                content=content.strip(),
                status='approved'
            )

            db.session.add(comment)
            db.session.commit()

            return comment.to_dict(), None

        except Exception as e:
            db.session.rollback()
            return None, f'Failed to submit comment: {str(e)}'

    def get_user_comments(self, user_id, page=1, per_page=20):
        """Get all comments created by a specific user"""
        pagination = Comment.query.filter_by(author_id=user_id) \
            .order_by(Comment.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'comments': [c.to_dict(include_email=True) for c in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def update_user_comment(self, comment_id, user_id, content):
        """Update a comment owned by the user"""
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                return None, 'Comment not found'

            if comment.author_id != int(user_id):
                return None, 'Access denied'

            if not content or len(content.strip()) < 5:
                return None, 'Comment must be at least 5 characters'

            comment.content = content.strip()
            comment.updated_at = datetime.utcnow()

            db.session.commit()
            return comment.to_dict(), None

        except Exception as e:
            db.session.rollback()
            return None, f'Failed to update comment: {str(e)}'

    def delete_user_comment(self, comment_id, user_id):
        """Delete a comment owned by the user"""
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                return False, 'Comment not found'

            if comment.author_id != int(user_id):
                return False, 'Access denied'

            db.session.delete(comment)
            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete comment: {str(e)}'

    # ======================================================
    # ADMIN
    # ======================================================

    def get_all_comments(self, page=1, per_page=20, status=None):
        """Get all comments (admin view)"""
        query = Comment.query.order_by(Comment.created_at.desc())

        if status:
            query = query.filter_by(status=status)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'comments': [c.to_dict(include_email=True) for c in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def get_pending_count(self):
        """Get count of pending comments"""
        return Comment.query.filter_by(status='pending').count()

    def moderate_comment(self, comment_id, action):
        """Approve or reject a comment"""
        try:
            if action not in ['approve', 'reject']:
                return None, 'Invalid action'

            comment = Comment.query.get(comment_id)
            if not comment:
                return None, 'Comment not found'

            comment.status = 'approved' if action == 'approve' else 'rejected'
            comment.moderated_at = datetime.utcnow()

            db.session.commit()
            return comment.to_dict(include_email=True), None

        except Exception as e:
            db.session.rollback()
            return None, f'Failed to moderate comment: {str(e)}'

    def admin_update_comment(self, comment_id, content):
        """Admin can update any comment (guest or user)"""
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                return None, 'Comment not found'

            if not content or len(content.strip()) < 5:
                return None, 'Comment must be at least 5 characters'

            comment.content = content.strip()
            comment.updated_at = datetime.utcnow()

            db.session.commit()
            return comment.to_dict(include_email=True), None

        except Exception as e:
            db.session.rollback()
            return None, f'Failed to update comment: {str(e)}'

    def delete_comment(self, comment_id):
        """Admin delete any comment"""
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                return False, 'Comment not found'

            db.session.delete(comment)
            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete comment: {str(e)}'
