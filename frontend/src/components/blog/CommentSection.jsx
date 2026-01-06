import { useState, useEffect } from 'react';
import commentService from '../../services/commentService';
import { useAuth } from '../../context/AuthContext';
import './CommentSection.css';

function CommentSection({ postId }) {
    const { user: authUser } = useAuth();
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        guest_name: '',
        guest_email: '',
        content: '',
    });

    useEffect(() => {
        loadComments();
    }, [postId]);

    const loadComments = async () => {
        try {
            setLoading(true);
            const data = await commentService.getComments(postId);
            setComments(data.comments || data || []);
        } catch (err) {
            console.error('Failed to load comments:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            setSubmitting(true);

            if (authUser) {
                await commentService.submitUserComment(postId, formData.content);
                setSuccess('✅ Your comment has been posted successfully!');
            } else {
                await commentService.submitComment(
                    postId,
                    formData.guest_name,
                    formData.guest_email,
                    formData.content
                );
                setSuccess('✅ Your comment has been submitted! It will appear after admin approval.');
            }

            setFormData({ guest_name: '', guest_email: '', content: '' });
            loadComments();

            document
                .querySelector('.comment-form-container')
                ?.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (err) {
            setError(err.response?.data?.error || 'Failed to submit comment');
        } finally {
            setSubmitting(false);
        }
    };

    const formatDate = (dateString) =>
        new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });

    return (
        <section className="comment-section">
            <h3 className="comment-section-title">
                Comments ({comments.length})
            </h3>

            {/* Comment Form */}
            <div className="comment-form-container">
                <h4>Leave a Comment</h4>
                <p className="comment-form-note">
                    Your email address will not be published. Comments are moderated before appearing.
                </p>

                {success && <div className="alert alert-success">{success}</div>}
                {error && <div className="alert alert-error">{error}</div>}

                <form onSubmit={handleSubmit} className="comment-form">
                    {!authUser && (
                        <div className="form-row">
                            <div className="form-group">
                                <label>Name *</label>
                                <input
                                    name="guest_name"
                                    value={formData.guest_name}
                                    onChange={handleChange}
                                    required
                                    disabled={submitting}
                                />
                            </div>
                            <div className="form-group">
                                <label>Email *</label>
                                <input
                                    type="email"
                                    name="guest_email"
                                    value={formData.guest_email}
                                    onChange={handleChange}
                                    required
                                    disabled={submitting}
                                />
                            </div>
                        </div>
                    )}

                    {authUser && (
                        <div className="user-info-hint">
                            Posting as <strong>{authUser.username}</strong>
                        </div>
                    )}

                    <div className="form-group">
                        <label>Comment *</label>
                        <textarea
                            name="content"
                            rows="4"
                            value={formData.content}
                            onChange={handleChange}
                            required
                            disabled={submitting}
                        />
                    </div>

                    <button type="submit" className="btn btn-primary" disabled={submitting}>
                        {submitting ? 'Submitting...' : 'Post Comment'}
                    </button>
                </form>
            </div>

            {/* Comments List */}
            <div className="comments-list">
                {loading ? (
                    <div className="spinner"></div>
                ) : comments.length === 0 ? (
                    <p>No comments yet.</p>
                ) : (
                    comments.map((c) => (
                        <div key={c.id} className="comment">
                            <strong>{c.author_name || c.guest_name}</strong>
                            <span className="comment-date">{formatDate(c.created_at)}</span>
                            <p>{c.content}</p>
                        </div>
                    ))
                )}
            </div>
        </section>
    );
}

export default CommentSection;
