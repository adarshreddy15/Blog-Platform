"""
Post and Tag Models - Blog content management
"""
from datetime import datetime
from ..extensions import db
import re


# Many-to-many relationship table for posts and tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Tag(db.Model):
    """Tag model for categorizing posts"""
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)
    
    @staticmethod
    def generate_slug(name):
        """Generate URL-friendly slug from name"""
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'


class Post(db.Model):
    """Blog post model"""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    featured_image = db.Column(db.String(255))
    status = db.Column(db.String(20), default='draft')  # draft, published
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
                          backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                              cascade='all, delete-orphan')
    
    @staticmethod
    def generate_slug(title):
        """Generate URL-friendly slug from title"""
        slug = title.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def to_dict(self, include_content=True):
        """Convert post to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'status': self.status,
            'author_id': self.author_id,
            'author': self.author.username if self.author else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'comment_count': self.comments.filter_by(status='approved').count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
        if include_content:
            data['content'] = self.content
        return data
    
    def __repr__(self):
        return f'<Post {self.title}>'
