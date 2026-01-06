from ..models import User, Post, Comment

class AdminService:
    def get_dashboard_stats(self):
        return {
            "total_users": User.query.count(),               # 👈 ADD THIS
            "total_posts": Post.query.count(),
            "pending_comments": Comment.query.filter_by(status='pending').count()
        }
