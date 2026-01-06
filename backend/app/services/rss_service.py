"""
RSS Service - Generate RSS feed for blog posts
"""
from datetime import datetime
from ..models import Post
import PyRSS2Gen


class RSSService:
    """
    RSS feed service following IoC principle.
    Generates RSS 2.0 feed for published blog posts.
    """
    
    def generate_feed(self, base_url='http://localhost:5000', limit=20):
        """
        Generate RSS feed XML for published posts.
        
        Args:
            base_url: The base URL of the blog
            limit: Maximum number of posts to include
        
        Returns:
            str: RSS feed XML string
        """
        posts = Post.query.filter_by(status='published')\
            .order_by(Post.published_at.desc())\
            .limit(limit)\
            .all()
        
        items = []
        for post in posts:
            items.append(
                PyRSS2Gen.RSSItem(
                    title=post.title,
                    link=f"{base_url}/blog/{post.slug}",
                    description=post.excerpt or post.content[:300],
                    author=post.author.username if post.author else 'Admin',
                    guid=PyRSS2Gen.Guid(f"{base_url}/blog/{post.slug}"),
                    pubDate=post.published_at or post.created_at
                )
            )
        
        rss = PyRSS2Gen.RSS2(
            title="Blog Platform",
            link=base_url,
            description="Latest blog posts from our platform",
            lastBuildDate=datetime.utcnow(),
            items=items
        )
        
        return rss.to_xml('utf-8')
    
    def get_feed_info(self, base_url='http://localhost:5000'):
        """Get basic feed information"""
        post_count = Post.query.filter_by(status='published').count()
        latest_post = Post.query.filter_by(status='published')\
            .order_by(Post.published_at.desc())\
            .first()
        
        return {
            'title': 'Blog Platform RSS Feed',
            'url': f"{base_url}/api/rss",
            'post_count': post_count,
            'last_updated': latest_post.published_at.isoformat() if latest_post else None
        }
