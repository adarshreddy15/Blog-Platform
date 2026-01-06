import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';
import postService from '../../services/postService';
import './PostEditor.css';

function EditPostPage() {
    const navigate = useNavigate();
    const { id } = useParams();
    const quillRef = useRef(null);
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        excerpt: '',
        tags: '',
        status: 'draft',
        featured_image: '',
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const modules = {
        toolbar: [
            [{ header: [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ list: 'ordered' }, { list: 'bullet' }],
            ['blockquote', 'code-block'],
            ['link', 'image'],
            ['clean'],
        ],
    };

    const formats = [
        'header',
        'bold', 'italic', 'underline', 'strike',
        'list', 'bullet',
        'blockquote', 'code-block',
        'link', 'image',
    ];

    useEffect(() => {
        loadPost();
    }, [id]);

    const loadPost = async () => {
        try {
            setLoading(true);
            const post = await postService.getPostById(id);
            setFormData({
                title: post.title || '',
                content: post.content || '',
                excerpt: post.excerpt || '',
                tags: post.tags?.map((t) => t.name).join(', ') || '',
                status: post.status || 'draft',
                featured_image: post.featured_image || '',
            });
        } catch (err) {
            setError('Failed to load post');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleContentChange = (value) => {
        setFormData((prev) => ({ ...prev, content: value }));
    };

    const handleImageUpload = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        try {
            setUploading(true);
            const data = await postService.uploadImage(file);
            setFormData((prev) => ({ ...prev, featured_image: data.image_url }));
        } catch (err) {
            setError('Failed to upload image');
        } finally {
            setUploading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!formData.title.trim() || !formData.content.trim()) {
            setError('Title and content are required');
            return;
        }

        try {
            setSaving(true);
            const tags = formData.tags
                .split(',')
                .map((t) => t.trim())
                .filter((t) => t);

            await postService.updatePost(id, {
                title: formData.title,
                content: formData.content,
                excerpt: formData.excerpt,
                tags,
                status: formData.status,
                featured_image: formData.featured_image,
            });

            setSuccess('Post updated successfully!');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to update post');
        } finally {
            setSaving(false);
        }
    };

    const imagePreview = formData.featured_image
        ? `http://localhost:5000${formData.featured_image}`
        : null;

    if (loading) {
        return (
            <div className="post-editor-page">
                <div className="loading-container">
                    <div className="spinner spinner-lg"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="post-editor-page">
            <header className="page-header">
                <div>
                    <h1>Edit Post</h1>
                    <p className="page-subtitle">Update your blog article</p>
                </div>
            </header>

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <form onSubmit={handleSubmit} className="post-editor-form">
                <div className="editor-main">
                    <div className="form-group">
                        <label htmlFor="title" className="form-label">Title</label>
                        <input
                            type="text"
                            id="title"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            className="form-input title-input"
                            placeholder="Enter post title..."
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Content</label>
                        <ReactQuill
                            ref={quillRef}
                            theme="snow"
                            value={formData.content}
                            onChange={handleContentChange}
                            modules={modules}
                            formats={formats}
                            placeholder="Write your post content here..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="excerpt" className="form-label">
                            Excerpt <span className="text-muted">(optional)</span>
                        </label>
                        <textarea
                            id="excerpt"
                            name="excerpt"
                            value={formData.excerpt}
                            onChange={handleChange}
                            className="form-textarea"
                            placeholder="Brief description of the post..."
                            rows="3"
                        ></textarea>
                    </div>
                </div>

                <div className="editor-sidebar">
                    <div className="sidebar-card">
                        <h3>Publish Settings</h3>

                        <div className="form-group">
                            <label htmlFor="status" className="form-label">Status</label>
                            <select
                                id="status"
                                name="status"
                                value={formData.status}
                                onChange={handleChange}
                                className="form-select"
                            >
                                <option value="draft">Draft</option>
                                <option value="published">Published</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="tags" className="form-label">
                                Tags <span className="text-muted">(comma separated)</span>
                            </label>
                            <input
                                type="text"
                                id="tags"
                                name="tags"
                                value={formData.tags}
                                onChange={handleChange}
                                className="form-input"
                                placeholder="tech, react, web"
                            />
                        </div>

                        <div className="form-actions">
                            <button
                                type="submit"
                                className="btn btn-primary w-full"
                                disabled={saving}
                            >
                                {saving ? 'Saving...' : 'Save Changes'}
                            </button>
                            <button
                                type="button"
                                onClick={() => navigate('/admin/posts')}
                                className="btn btn-outline w-full"
                            >
                                Back to Posts
                            </button>
                        </div>
                    </div>

                    <div className="sidebar-card">
                        <h3>Featured Image</h3>

                        {imagePreview && (
                            <div className="image-preview">
                                <img src={imagePreview} alt="Featured" />
                                <button
                                    type="button"
                                    className="btn btn-danger btn-sm remove-image"
                                    onClick={() => setFormData((prev) => ({ ...prev, featured_image: '' }))}
                                >
                                    Remove
                                </button>
                            </div>
                        )}

                        <div className="form-group">
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handleImageUpload}
                                className="form-input"
                                disabled={uploading}
                            />
                            {uploading && <span className="upload-status">Uploading...</span>}
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default EditPostPage;
