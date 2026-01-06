import { Link } from 'react-router-dom';
import './TagFilter.css';

function TagFilter({ tags, activeTag = null, loading = false }) {
    if (loading) {
        return (
            <div className="tag-filter">
                <div className="spinner"></div>
            </div>
        );
    }

    if (!tags || tags.length === 0) {
        return null;
    }

    return (
        <div className="tag-filter">
            <h3 className="tag-filter-title">Browse by Topic</h3>
            <div className="tag-filter-list">
                <Link
                    to="/"
                    className={`tag-filter-item ${!activeTag ? 'active' : ''}`}
                >
                    All Posts
                </Link>
                {tags.map((tag) => (
                    <Link
                        key={tag.id}
                        to={`/tag/${tag.slug}`}
                        className={`tag-filter-item ${activeTag === tag.slug ? 'active' : ''}`}
                    >
                        {tag.name}
                        {tag.post_count > 0 && (
                            <span className="tag-count">{tag.post_count}</span>
                        )}
                    </Link>
                ))}
            </div>
        </div>
    );
}

export default TagFilter;
