"""
Post Service - Blog post CRUD operations
"""
from datetime import datetime
from ..models import Post, Tag
from ..extensions import db
from ..utils import save_image, delete_image


class PostService:
    """
    Post service following IoC principle.
    All post-related business logic is encapsulated here.
    """
    
    def get_published_posts(self, page=1, per_page=10):
        """Get paginated list of published posts"""
        pagination = Post.query.filter_by(status='published')\
            .order_by(Post.published_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'posts': [post.to_dict(include_content=False) for post in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    def get_all_posts(self, page=1, per_page=10, status=None):
        """Get all posts (admin view) with optional status filter"""
        query = Post.query.order_by(Post.created_at.desc())

        if status:
            query = query.filter_by(status=status)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'posts': [post.to_dict(include_content=False) for post in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def get_user_posts(self, user_id, page=1, per_page=10, status=None):
        """Get posts created by a specific user"""
        query = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc())

        if status:
            query = query.filter_by(status=status)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'posts': [post.to_dict(include_content=False) for post in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def get_post_by_slug(self, slug, published_only=True):
        """Get a single post by slug"""
        query = Post.query.filter_by(slug=slug)
        
        if published_only:
            query = query.filter_by(status='published')
        
        post = query.first()
        return post.to_dict() if post else None
    
    def get_post_by_id(self, post_id):
        """Get a single post by ID (admin)"""
        post = Post.query.get(post_id)
        return post.to_dict() if post else None
    
    def get_posts_by_tag(self, tag_slug, page=1, per_page=10):
        """Get published posts filtered by tag"""
        tag = Tag.query.filter_by(slug=tag_slug).first()
        
        if not tag:
            return {
                'posts': [],
                'total': 0,
                'pages': 0,
                'current_page': page,
                'tag': None
            }
        
        pagination = Post.query.filter(
            Post.tags.contains(tag),
            Post.status == 'published'
        ).order_by(Post.published_at.desc())\
         .paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'posts': [post.to_dict(include_content=False) for post in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'tag': tag.to_dict()
        }
    
    def create_post(self, title, content, author_id, excerpt=None, tags=None, 
                    featured_image=None, status='draft'):
        """Create a new blog post"""
        try:
            # Generate unique slug
            base_slug = Post.generate_slug(title)
            slug = base_slug
            counter = 1
            while Post.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            post = Post(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt or content[:200] + '...' if len(content) > 200 else content,
                author_id=author_id,
                status=status,
                featured_image=featured_image
            )
            
            # Set published_at if publishing
            if status == 'published':
                post.published_at = datetime.utcnow()
            
            # Handle tags
            if tags:
                post.tags = self._process_tags(tags)
            
            db.session.add(post)
            db.session.commit()
            
            return post.to_dict(), None
        
        except Exception as e:
            db.session.rollback()
            return None, f'Failed to create post: {str(e)}'
    
    def update_post(self, post_id, **kwargs):
        """Update an existing post"""
        try:
            post = Post.query.get(post_id)
            if not post:
                return None, 'Post not found'
            
            # Update fields
            if 'title' in kwargs:
                post.title = kwargs['title']
                # Regenerate slug if title changed
                base_slug = Post.generate_slug(kwargs['title'])
                if base_slug != post.slug.rsplit('-', 1)[0]:
                    slug = base_slug
                    counter = 1
                    while Post.query.filter(Post.slug == slug, Post.id != post_id).first():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    post.slug = slug
            
            if 'content' in kwargs:
                post.content = kwargs['content']
            
            if 'excerpt' in kwargs:
                post.excerpt = kwargs['excerpt']
            
            if 'featured_image' in kwargs:
                # Delete old image if exists
                if post.featured_image and post.featured_image != kwargs['featured_image']:
                    delete_image(post.featured_image)
                post.featured_image = kwargs['featured_image']
            
            if 'status' in kwargs:
                # Set published_at when first published
                if kwargs['status'] == 'published' and post.status != 'published':
                    post.published_at = datetime.utcnow()
                post.status = kwargs['status']
            
            if 'tags' in kwargs:
                post.tags = self._process_tags(kwargs['tags'])
            
            db.session.commit()
            return post.to_dict(), None
        
        except Exception as e:
            db.session.rollback()
            return None, f'Failed to update post: {str(e)}'
    
    def delete_post(self, post_id):
        """Delete a post"""
        try:
            post = Post.query.get(post_id)
            if not post:
                return False, 'Post not found'
            
            # Delete featured image
            if post.featured_image:
                delete_image(post.featured_image)
            
            db.session.delete(post)
            db.session.commit()
            return True, None
        
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete post: {str(e)}'
    
    def upload_image(self, file):
        """Upload an image for a post"""
        image_path = save_image(file, 'posts')
        if image_path:
            return {'image_url': image_path}, None
        return None, 'Failed to upload image'
    
    def get_all_tags(self):
        """Get all tags with post counts"""
        tags = Tag.query.all()
        return [{
            **tag.to_dict(),
            'post_count': tag.posts.filter_by(status='published').count()
        } for tag in tags]
    
    def _process_tags(self, tag_names):
        """Process tag names and return Tag objects"""
        tags = []
        for name in tag_names:
            name = name.strip()
            if not name:
                continue
            
            slug = Tag.generate_slug(name)
            tag = Tag.query.filter_by(slug=slug).first()
            
            if not tag:
                tag = Tag(name=name, slug=slug)
                db.session.add(tag)
            
            tags.append(tag)
        
        return tags
