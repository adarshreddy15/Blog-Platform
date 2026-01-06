import { useEffect } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './UserLayout.css';

function UserLayout() {
    const navigate = useNavigate();
    const location = useLocation();
    const { user, logout, isAuthenticated, loading } = useAuth();

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            navigate('/login', { replace: true });
        }
    }, [isAuthenticated, loading, navigate]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const isActive = (path) => {
        if (path === '/dashboard' && location.pathname === '/dashboard') return true;
        if (path !== '/dashboard' && location.pathname.startsWith(path)) return true;
        return false;
    };

    if (loading) {
        return (
            <div className="user-loading">
                <div className="spinner spinner-lg"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className="user-layout">
            {/* Sidebar */}
            <aside className="user-sidebar">
                <div className="sidebar-header">
                    <Link to="/" className="user-logo">
                        <span className="logo-icon">✦</span>
                        <span>User Portal</span>
                    </Link>
                </div>

                <nav className="sidebar-nav">
                    <Link
                        to="/"
                        className="nav-item"
                    >
                        <span className="nav-icon">🏠</span>
                        Back to Blog
                    </Link>
                    <Link
                        to="/dashboard"
                        className={`nav-item ${isActive('/dashboard') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">📊</span>
                        Dashboard
                    </Link>
                    <Link
                        to="/user/posts"
                        className={`nav-item ${isActive('/user/posts') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">📝</span>
                        My Posts
                    </Link>
                    <Link
                        to="/user/posts/create"
                        className={`nav-item ${isActive('/user/posts/create') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">✏️</span>
                        Create Post
                    </Link>
                    <Link
                        to="/user/comments"
                        className={`nav-item ${isActive('/user/comments') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">💬</span>
                        My Comments
                    </Link>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-info">
                        <div className="user-avatar">
                            {user?.username?.charAt(0).toUpperCase() || 'U'}
                        </div>
                        <div className="user-details">
                            <span className="user-name">{user?.username || 'User'}</span>
                            <span className="user-role">Member</span>
                        </div>
                    </div>
                    <button onClick={handleLogout} className="btn btn-outline btn-sm logout-btn">
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="user-main">
                <div className="user-content">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}

export default UserLayout;
