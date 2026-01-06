import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import authService from '../../services/authService';
import './DashboardPage.css';

function DashboardPage() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboard();
    }, []);

    const loadDashboard = async () => {
        try {
            setLoading(true);
            const data = await authService.getDashboard();
            setStats(data.stats);
        } catch (err) {
            console.error('Failed to load dashboard:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner spinner-lg"></div>
            </div>
        );
    }

    return (
        <div className="dashboard-page">
            <header className="page-header">
                <h1>Dashboard</h1>
                <p className="page-subtitle">
                    Welcome back! Here's an overview of your blog.
                </p>
            </header>

            {/* ===== Stats Cards ===== */}
            <div className="stats-grid">

                {/* Total Posts */}
                <div className="stat-card">
                    <div className="stat-icon">📝</div>
                    <div className="stat-content">
                        <span className="stat-value">{stats?.total_posts || 0}</span>
                        <span className="stat-label">Total Posts</span>
                    </div>
                    <Link to="/admin/posts" className="stat-link">
                        View all →
                    </Link>
                </div>

                {/* Pending Comments */}
                <div className="stat-card pending">
                    <div className="stat-icon">💬</div>
                    <div className="stat-content">
                        <span className="stat-value">
                            {stats?.pending_comments || 0}
                        </span>
                        <span className="stat-label">Pending Comments</span>
                    </div>
                    <Link to="/admin/comments" className="stat-link">
                        Moderate →
                    </Link>
                </div>

                {/* ✅ Total Users (NEW) */}
                <div className="stat-card users">
                    <div className="stat-icon">👤</div>
                    <div className="stat-content">
                        <span className="stat-value">
                            {stats?.total_users || 0}
                        </span>
                        <span className="stat-label">Total Users</span>
                    </div>
                    <Link to="/admin/users" className="stat-link">
                        View users →
                    </Link>
                </div>

            </div>

            {/* ===== Quick Actions ===== */}
            <section className="quick-actions">
                <h2>Quick Actions</h2>
                <div className="actions-grid">

                    <Link to="/admin/posts/create" className="action-card">
                        <span className="action-icon">✏️</span>
                        <span className="action-title">Create New Post</span>
                        <span className="action-desc">
                            Write and publish a new blog article
                        </span>
                    </Link>

                    <Link to="/admin/posts" className="action-card">
                        <span className="action-icon">📁</span>
                        <span className="action-title">Manage Posts</span>
                        <span className="action-desc">
                            Edit, delete, or change post status
                        </span>
                    </Link>

                    <Link to="/admin/comments" className="action-card">
                        <span className="action-icon">✓</span>
                        <span className="action-title">Review Comments</span>
                        <span className="action-desc">
                            Approve or reject pending comments
                        </span>
                    </Link>

                    <Link to="/" className="action-card">
                        <span className="action-icon">🌐</span>
                        <span className="action-title">View Blog</span>
                        <span className="action-desc">
                            See your blog as visitors do
                        </span>
                    </Link>

                </div>
            </section>
        </div>
    );
}

export default DashboardPage;
