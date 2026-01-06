import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-brand">
                        <Link to="/" className="footer-logo">
                            <span className="logo-icon">✦</span>
                            <span>Blog Platform</span>
                        </Link>
                        <p className="footer-tagline">
                            Sharing ideas, stories, and knowledge with the world.
                        </p>
                    </div>

                    <div className="footer-links">
                        <div className="footer-section">
                            <h4>Quick Links</h4>
                            <ul>
                                <li><Link to="/">Home</Link></li>
                                <li><a href="/api/rss" target="_blank" rel="noopener noreferrer">RSS Feed</a></li>
                            </ul>
                        </div>

                        <div className="footer-section">
                            <h4>Admin</h4>
                            <ul>
                                <li><Link to="/admin/login">Login</Link></li>
                                <li><Link to="/admin/register">Register</Link></li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>© {currentYear} Blog Platform. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
