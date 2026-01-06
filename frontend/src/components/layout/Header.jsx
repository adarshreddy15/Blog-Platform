import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

function Header() {
    const { user, logout } = useAuth();

    return (
        <header className="header">
            <div className="container">
                <div className="header-content">
                    <Link to="/" className="logo">
                        <span className="logo-icon">✦</span>
                        <span className="logo-text">Blog Platform</span>
                    </Link>

                    <nav className="nav">
                        <Link to="/" className="nav-link">Home</Link>
                        <a href="http://localhost:5000/api/rss" target="_blank" rel="noopener noreferrer" className="nav-link">
                            RSS Feed
                        </a>

                        {user ? (
                            <>
                                <Link to={user.is_admin ? "/admin" : "/dashboard"} className="nav-link">
                                    {user.is_admin ? "Admin Panel" : "Dashboard"}
                                </Link>
                                <span className="nav-link" style={{cursor: 'default'}}>
                                    {user.username}
                                </span>
                                <button onClick={logout} className="btn btn-outline btn-sm">
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="btn btn-outline btn-sm">
                                    User Login
                                </Link>
                                <Link to="/admin/login" className="btn btn-outline btn-sm">
                                    Admin Login
                                </Link>
                            </>
                        )}
                    </nav>
                </div>
            </div>
        </header>
    );
}

export default Header;
