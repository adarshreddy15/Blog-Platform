import PostCard from './PostCard';
import './PostList.css';

function PostList({ posts, loading, emptyMessage = 'No posts found.' }) {
    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner spinner-lg"></div>
            </div>
        );
    }

    if (!posts || posts.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-icon">📝</div>
                <h3>No Posts Yet</h3>
                <p>{emptyMessage}</p>
            </div>
        );
    }

    return (
        <div className="post-list grid grid-3">
            {posts.map((post) => (
                <PostCard key={post.id} post={post} />
            ))}
        </div>
    );
}

export default PostList;
