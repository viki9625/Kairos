'use client';

import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        const userId = localStorage.getItem('userId');
        if (token && userId) {
            setUser({ token, userId });
        }
        setLoading(false);
    }, []);

    const logout = () => {
        // --- DEBUGGING: Checkpoint A ---
        console.log("AuthContext: logout() function has been called.");
        
        localStorage.removeItem('accessToken');
        localStorage.removeItem('userId');
        
        // --- DEBUGGING: Checkpoint B ---
        console.log("AuthContext: localStorage has been cleared.");

        setUser(null);
        
        // --- DEBUGGING: Checkpoint C ---
        console.log("AuthContext: Global user state has been set to null.");
    };

    return (
        <AuthContext.Provider value={{ user, setUser, loading, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);

