/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const storedUser = authService.getUser();
        if (storedUser && authService.isAuthenticated()) {
            setUser(storedUser);
        }
        setLoading(false);
    }, []);

    // ✅ ADMIN LOGIN (used by AdminLoginPage)
    const login = async (email, password) => {
        const data = await authService.adminLogin(email, password);
        authService.setAuth(data.access_token, data.user);
        setUser(data.user);
        return data;
    };

    // ✅ USER LOGIN (use in UserLoginPage)
    const userLogin = async (email, password) => {
        const data = await authService.userLogin(email, password);
        authService.setAuth(data.access_token, data.user);
        setUser(data.user);
        return data;
    };

    // ✅ USER REGISTER
    const register = async (email, username, password) => {
        const data = await authService.userRegister(email, username, password);
        return data;
    };

    // ✅ LOGOUT
    const logout = () => {
        authService.clearAuth();
        setUser(null);
    };

    const value = {
        user,
        loading,
        login,        // Admin login
        userLogin,    // User login
        register,
        logout,
        isAuthenticated: !!user,
        isAdmin: user?.is_admin === true
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

export default AuthContext;
