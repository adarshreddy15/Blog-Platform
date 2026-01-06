import { useState, useEffect } from 'react';
import commentService from '../../services/commentService';
import './CommentsPage.css';

function CommentsPage() {
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [statusFilter, setStatusFilter] = useState('');
    const [actionLoading, setActionLoading] = useState(null);

    // ✏️ Edit state
    const [editingId, setEditingId] = useState(null);
    const [editContent, setEditContent] = useState('');

    useEffect(() => {
        loadComments();
    }, [page, statusFilter]);

    const loadComments = async () => {
        try {
            setLoading(true);
            const data = await commentService.getAllComments(page, 20, statusFilter || null);
            setComments(data.comments || []);
            setTotalPages(data.pages || 1);
        } catch (err) {
            console.error('Failed to load comments:', err);
        } finally {
            setLoading(false);
        }
    };

    // ✅ Approve / Reject
    const handleModerate = async (id, action) => {
        try {
            setActionLoading(id);
            await commentService.moderateComment(id, action);
            await loadComments();
        } catch (err) {
            alert(err.response?.data?.error || 'Failed to moderate comment');
        } finally {
            setActionLoading(null);
        }
    };

    // 🗑 Delete
    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this comment?')) return;

        try {
            setActionLoading(id);
            await commentService.deleteComment(id);
            await loadComments();
        } catch (err) {
            alert(err.response?.data?.error || 'Failed to delete comment');
        } finally {
            setActionLoading(null);
        }
    };

    // ✏️ Start edit
    const startEdit = (comment) => {
        setEditingId(comment.id);
        setEditContent(comment.content);
    };

    // ❌ Cancel edit
    const cancelEdit = () => {
        setEditingId(null);
        setEditContent('');
    };

    // 💾 Save edit (ADMIN)
    const saveEdit = async (id) => {
        if (!editContent.trim() || editContent.trim().length < 5) {
            alert('Comment must be at least 5 characters');
            return;
        }

        try {
            setActionLoading(id);
            await commentService.updateCommentAdmin(id, editContent.trim());
            setEditingId(null);
            setEditContent('');
            await loadComments();
        } catch (err) {
            console.error(err);
            alert(err.response?.data?.error || 'Failed to update comment');
        } finally {
            setActionLoading(null);
        }
    };

    const formatDate = (dateString) =>
        new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });

    const getStatusBadge = (status) => {
        const map = {
            pending: 'badge-warning',
            approved: 'badge-success',
            rejected: 'badge-error',
        };
        return <span className={`badge ${map[status]}`}>{status}</span>;
    };

    return (
        <div className="comments-page">
            <header className="page-header">
                <h1>Comments</h1>
                <p className="page-subtitle">Moderate & manage comments</p>
            </header>

            {/* Filters */}
            <div className="filters">
                <select
                    value={statusFilter}
                    onChange={(e) => {
                        setStatusFilter(e.target.value);
                        setPage(1);
                    }}
                    className="form-select"
                >
                    <option value="">All Comments</option>
                    <option value="pending">Pending</option>
                    <option value="approved">Approved</option>
                    <option value="rejected">Rejected</option>
                </select>
            </div>

            {/* Content */}
            {loading ? (
                <div className="loading-container">
                    <div className="spinner" />
                </div>
            ) : comments.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">💬</div>
                    <h3>No Comments Found</h3>
                </div>
            ) : (
                <div className="comments-list">
                    {comments.map((c) => (
                        <div key={c.id} className="comment-card">
                            <div className="comment-header">
                                <div>
                                    <strong>{c.author_name || c.guest_name}</strong>
                                    {!c.is_guest && <span className="user-badge ml-1">User</span>}
                                    <div className="comment-email">
                                        {c.author_email || c.guest_email}
                                    </div>
                                </div>
                                <div>
                                    {getStatusBadge(c.status)}
                                    <div className="comment-date">
                                        {formatDate(c.created_at)}
                                    </div>
                                </div>
                            </div>

                            <div className="comment-body">
                                {editingId === c.id ? (
                                    <textarea
                                        className="form-textarea"
                                        rows="3"
                                        value={editContent}
                                        onChange={(e) => setEditContent(e.target.value)}
                                        disabled={actionLoading === c.id}
                                    />
                                ) : (
                                    <p>{c.content}</p>
                                )}
                            </div>

                            <div className="comment-footer">
                                <span>Post #{c.post_id}</span>

                                <div className="comment-actions">
                                    {editingId === c.id ? (
                                        <>
                                            <button
                                                className="btn btn-success btn-sm"
                                                onClick={() => saveEdit(c.id)}
                                                disabled={actionLoading === c.id}
                                            >
                                                Save
                                            </button>
                                            <button
                                                className="btn btn-outline btn-sm"
                                                onClick={cancelEdit}
                                                disabled={actionLoading === c.id}
                                            >
                                                Cancel
                                            </button>
                                        </>
                                    ) : (
                                        <>
                                            <button
                                                className="btn btn-outline btn-sm"
                                                onClick={() => startEdit(c)}
                                            >
                                                Edit
                                            </button>

                                            {c.status !== 'approved' && (
                                                <button
                                                    className="btn btn-success btn-sm"
                                                    onClick={() => handleModerate(c.id, 'approve')}
                                                    disabled={actionLoading === c.id}
                                                >
                                                    Approve
                                                </button>
                                            )}

                                            {c.status !== 'rejected' && (
                                                <button
                                                    className="btn btn-outline btn-sm"
                                                    onClick={() => handleModerate(c.id, 'reject')}
                                                    disabled={actionLoading === c.id}
                                                >
                                                    Reject
                                                </button>
                                            )}

                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDelete(c.id)}
                                                disabled={actionLoading === c.id}
                                            >
                                                Delete
                                            </button>
                                        </>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
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
                    <span>
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

export default CommentsPage;
