import { useEffect } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AdminLayout.css';

function AdminLayout() {
    const navigate = useNavigate();
    const location = useLocation();
    const { user, logout, isAuthenticated, loading } = useAuth();

    useEffect(() => {
        // Only redirect if we ARE NOT loading AND we ARE NOT authenticated
        if (!loading && !isAuthenticated) {
            console.log('Not authenticated, redirecting to login');
            navigate('/admin/login', { replace: true });
        }
    }, [isAuthenticated, loading, navigate]);

    const handleLogout = () => {
        logout();
        navigate('/admin/login');
    };

    const isActive = (path) => {
        if (path === '/admin' && location.pathname === '/admin') return true;
        if (path !== '/admin' && location.pathname.startsWith(path)) return true;
        return false;
    };

    if (loading) {
        return (
            <div className="admin-loading">
                <div className="spinner spinner-lg"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className="admin-layout">
            {/* Sidebar */}
            <aside className="admin-sidebar">
                <div className="sidebar-header">
                    <Link to="/" className="admin-logo">
                        <span className="logo-icon">✦</span>
                        <span>Blog Admin</span>
                    </Link>
                </div>

                <nav className="sidebar-nav">
                    <Link
                        to="/"
                        className="nav-item"
                    >
                        <span className="nav-icon">🏠</span>
                        Back to Home
                    </Link>
                    <Link
                        to="/admin"
                        className={`nav-item ${isActive('/admin') && location.pathname === '/admin' ? 'active' : ''}`}
                    >
                        <span className="nav-icon">📊</span>
                        Dashboard
                    </Link>
                    <Link
                        to="/admin/posts"
                        className={`nav-item ${isActive('/admin/posts') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">📝</span>
                        Posts
                    </Link>
                    <Link
                        to="/admin/posts/create"
                        className={`nav-item ${isActive('/admin/posts/create') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">✏️</span>
                        Create Post
                    </Link>
                    <Link
                        to="/admin/comments"
                        className={`nav-item ${isActive('/admin/comments') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">💬</span>
                        Comments
                    </Link>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-info">
                        <div className="user-avatar">
                            {user?.username?.charAt(0).toUpperCase() || 'A'}
                        </div>
                        <div className="user-details">
                            <span className="user-name">{user?.username || 'Admin'}</span>
                            <span className="user-role">Administrator</span>
                        </div>
                    </div>
                    <button onClick={handleLogout} className="btn btn-outline btn-sm logout-btn">
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="admin-main">
                <div className="admin-content">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}

export default AdminLayout;
