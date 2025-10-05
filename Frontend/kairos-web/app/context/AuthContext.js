'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for user credentials in local storage when the app loads
        const token = localStorage.getItem('accessToken');
        const userId = localStorage.getItem('userId');
        if (token && userId) {
            setUser({ token, userId });
        }
        setLoading(false);
    }, []);

    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('userId');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, setUser, loading, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook to use the auth context easily in other components
export const useAuth = () => useContext(AuthContext);
