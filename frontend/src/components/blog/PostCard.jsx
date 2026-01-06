import { Link } from 'react-router-dom';
import './PostCard.css';

function PostCard({ post }) {
    const formatDate = (dateString) => {
        if (!dateString) return '';
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    };

    const imageUrl = post.featured_image
        ? `http://localhost:5000${post.featured_image}`
        : 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600&h=400&fit=crop';

    return (
        <article className="post-card card">
            <Link to={`/blog/${post.slug}`} className="post-card-image-link">
                <img
                    src={imageUrl}
                    alt={post.title}
                    className="post-card-image"
                    onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600&h=400&fit=crop';
                    }}
                />
            </Link>

            <div className="card-body">
                {post.tags && post.tags.length > 0 && (
                    <div className="tags mb-2">
                        {post.tags.slice(0, 3).map((tag) => (
                            <Link key={tag.id} to={`/tag/${tag.slug}`} className="tag">
                                {tag.name}
                            </Link>
                        ))}
                    </div>
                )}

                <h3 className="card-title">
                    <Link to={`/blog/${post.slug}`}>{post.title}</Link>
                </h3>

                <p className="card-text">{post.excerpt}</p>

                <div className="card-meta">
                    <span className="post-author">By {post.author}</span>
                    <span className="post-date">{formatDate(post.published_at || post.created_at)}</span>
                    {post.comment_count > 0 && (
                        <span className="post-comments">
                            {post.comment_count} comment{post.comment_count !== 1 ? 's' : ''}
                        </span>
                    )}
                </div>
            </div>
        </article>
    );
}

export default PostCard;
