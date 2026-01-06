"""
Comment Model - Guest commenting system with moderation
"""
from datetime import datetime
from ..extensions import db


class Comment(db.Model):
    """Comment model for both authenticated users and guests"""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Null for guest comments
    guest_name = db.Column(db.String(100), nullable=True)  # Only for guest comments
    guest_email = db.Column(db.String(120), nullable=True)  # Only for guest comments
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='approved')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    moderated_at = db.Column(db.DateTime)

    def to_dict(self, include_email=False):
        """Convert comment to dictionary"""
        # Determine author name - use username if authenticated, guest_name if not
        author_name = self.author.username if self.author_id and self.author else self.guest_name

        data = {
            'id': self.id,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'author_name': author_name,
            'is_guest': self.author_id is None,
            'content': self.content,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data['guest_email'] = self.guest_email
            data['author_email'] = self.author.email if self.author_id and self.author else None
            data['moderated_at'] = self.moderated_at.isoformat() if self.moderated_at else None
        return data

    def __repr__(self):
        author_name = self.author.username if self.author_id else self.guest_name
        return f'<Comment by {author_name}>'
