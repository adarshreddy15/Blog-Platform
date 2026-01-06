import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import postService from '../../services/postService';
import './PostsPage.css';

function PostsPage() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [statusFilter, setStatusFilter] = useState('');
    const [deleteId, setDeleteId] = useState(null);

    useEffect(() => {
        loadPosts();
    }, [page, statusFilter]);

    const loadPosts = async () => {
        try {
            setLoading(true);
            const data = await postService.getAllPosts(page, 10, statusFilter || null);
            setPosts(data.posts);
            setTotalPages(data.pages);
        } catch (err) {
            console.error('Failed to load posts:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this post?')) return;

        try {
            setDeleteId(id);
            await postService.deletePost(id);
            loadPosts();
        } catch (err) {
            alert('Failed to delete post: ' + (err.response?.data?.error || 'Unknown error'));
        } finally {
            setDeleteId(null);
        }
    };

    const handleStatusUpdate = async (id, newStatus) => {
        try {
            await postService.updatePost(id, { status: newStatus });
            loadPosts();
        } catch (err) {
            alert('Failed to update status: ' + (err.response?.data?.error || 'Unknown error'));
        }
    };

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    return (
        <div className="posts-page">
            <header className="page-header">
                <div>
                    <h1>Posts</h1>
                    <p className="page-subtitle">Manage your blog posts</p>
                </div>
                <Link to="/admin/posts/create" className="btn btn-primary">
                    + Create Post
                </Link>
            </header>

            {/* Filters */}
            <div className="filters">
                <select
                    value={statusFilter}
                    onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
                    className="form-select"
                >
                    <option value="">All Status</option>
                    <option value="published">Published</option>
                    <option value="draft">Drafts</option>
                </select>
            </div>

            {/* Posts Table */}
            {loading ? (
                <div className="loading-container">
                    <div className="spinner"></div>
                </div>
            ) : posts.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">📝</div>
                    <h3>No Posts Found</h3>
                    <p>Create your first blog post to get started.</p>
                    <Link to="/admin/posts/create" className="btn btn-primary">
                        Create Post
                    </Link>
                </div>
            ) : (
                <div className="table-container">
                    <table className="posts-table">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Status</th>
                                <th>Author</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {posts.map((post) => (
                                <tr key={post.id}>
                                    <td>
                                        <Link to={`/admin/posts/edit/${post.id}`} className="post-title-link">
                                            {post.title}
                                        </Link>
                                        {post.tags?.length > 0 && (
                                            <div className="post-tags">
                                                {post.tags.slice(0, 3).map((tag) => (
                                                    <span key={tag.id} className="tag-mini">{tag.name}</span>
                                                ))}
                                            </div>
                                        )}
                                    </td>
                                    <td>
                                        <span className={`badge badge-${post.status === 'published' ? 'success' : 'warning'}`}>
                                            {post.status}
                                        </span>
                                    </td>
                                    <td>{post.author}</td>
                                    <td>{formatDate(post.published_at || post.created_at)}</td>
                                    <td>
                                        <div className="actions">
                                            <Link
                                                to={`/admin/posts/edit/${post.id}`}
                                                className="btn btn-outline btn-sm"
                                            >
                                                Edit
                                            </Link>
                                            {post.status === 'draft' && (
                                                <button
                                                    onClick={() => handleStatusUpdate(post.id, 'published')}
                                                    className="btn btn-success btn-sm"
                                                >
                                                    Publish
                                                </button>
                                            )}
                                            <button
                                                onClick={() => handleDelete(post.id)}
                                                className="btn btn-danger btn-sm"
                                                disabled={deleteId === post.id}
                                            >
                                                {deleteId === post.id ? 'Deleting...' : 'Delete'}
                                            </button>
                                            {post.status === 'published' && (
                                                <Link
                                                    to={`/blog/${post.slug}`}
                                                    className="btn btn-secondary btn-sm"
                                                >
                                                    View
                                                </Link>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        className="btn btn-outline btn-sm"
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        disabled={page === 1}
                    >
                        ← Previous
                    </button>
                    <span className="pagination-info">
                        Page {page} of {totalPages}
                    </span>
                    <button
                        className="btn btn-outline btn-sm"
                        onClick={() => setPage((p) => p + 1)}
                        disabled={page >= totalPages}
                    >
                        Next →
                    </button>
                </div>
            )}
        </div>
    );
}

export default PostsPage;
