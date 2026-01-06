import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AuthPages.css';

function LoginPage() {
    const navigate = useNavigate();
    const { login, isAuthenticated, loading: authLoading } = useAuth();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [loginSuccess, setLoginSuccess] = useState(false);

    // Redirect if already logged in or just logged in successfully
    useEffect(() => {
        if (isAuthenticated || loginSuccess) {
            navigate('/admin', { replace: true });
        }
    }, [isAuthenticated, loginSuccess, navigate]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            setLoading(true);
            console.log('Attempting login for:', formData.email);
            const data = await login(formData.email, formData.password);
            console.log('Login API response:', data);

            if (data && data.access_token) {
                console.log('Login successful, setting success state');
                setLoginSuccess(true);
                // Direct navigation instead of waiting for useEffect if possible
                navigate('/admin', { replace: true });
            } else {
                setError('Login successful but no token received.');
            }
        } catch (err) {
            console.error('Login error detail:', err);
            const serverMessage = err.response?.data?.error || err.response?.data?.message || err.message;
            setError(`Login failed: ${serverMessage}`);
        } finally {
            setLoading(false);
        }
    };

    // Show loading while checking initial auth
    if (authLoading) {
        return (
            <div className="auth-page">
                <div className="loading-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
                    <div className="spinner spinner-lg"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="auth-page">
            <div className="auth-container">
                <div className="auth-card">
                    <div className="auth-header">
                        <Link to="/" className="auth-logo">
                            <span className="logo-icon">✦</span>
                            <span>Blog Platform</span>
                        </Link>
                        <h1>Admin Login</h1>
                        <p>Sign in to access the admin panel</p>
                    </div>

                    {error && <div className="alert alert-error">{error}</div>}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="email" className="form-label">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="form-input"
                                placeholder="admin@blog.com"
                                required
                                disabled={loading}
                                autoComplete="email"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="form-input"
                                placeholder="••••••••"
                                required
                                disabled={loading}
                                autoComplete="current-password"
                            />
                        </div>

                        <button type="submit" className="btn btn-primary btn-lg w-full" disabled={loading}>
                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    Signing in...
                                </>
                            ) : (
                                'Sign In'
                            )}
                        </button>
                    </form>

                    <div className="auth-footer">
                        <p>
                            Don't have an account?{' '}
                            <Link to="/admin/register">Register</Link>
                        </p>
                        <Link to="/" className="back-to-blog">
                            ← Back to Blog
                        </Link>
                    </div>

                    {/* <div style={{ marginTop: '20px', padding: '12px', background: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '8px', fontSize: '13px', color: '#666' }}>
                        <strong style={{ color: '#444' }}>💡 Testing Account:</strong><br />
                        If you haven't registered yet, use:<br />
                        Email: <code style={{ color: '#d63384' }}>admin@blog.com</code><br />
                        Password: <code style={{ color: '#d63384' }}>admin123</code>
                    </div> */}
                </div>
            </div>
        </div>
    );
}

export default LoginPage;
