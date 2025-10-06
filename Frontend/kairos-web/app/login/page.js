'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/context/AuthContext'; // <-- 1. Import the useAuth hook

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const { setUser } = useAuth(); // <-- 2. Get the setUser function from the context

    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_URL}/api/auth/token`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                // Save credentials to local storage
                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('userId', data.user_id);

                // --- THIS IS THE FIX ---
                // 3. Directly update the global authentication state
                setUser({ token: data.access_token, userId: data.user_id });
                // ----------------------

                // Now, redirect to the chatbot page
                router.push('/chatbot');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Failed to log in. Please check your credentials.');
            }
        } catch (err) {
            setError('An error occurred. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = () => {
        window.location.href = `${API_URL}/api/auth/google/login`;
    };

    return (
        // This outer container fills the available height and centers the form card.
        <div className="min-h-[86.4vh] bg-[#a7ebf2] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            {/* This is the form card. We removed the `space-y-8` class from here to prevent
              it from stretching vertically. We'll add spacing to the elements inside instead.
            */}
            <div className="max-w-md w-full bg-[#023859] p-8 md:p-10 rounded-xl shadow-2xl">
                
                <div>
                    <h2 className="text-center text-3xl font-extrabold text-[#a7ebf2]">
                        Welcome Back
                    </h2>
                    <p className="mt-2 text-center text-sm text-[#aff7ff]">
                        Log In to continue your wellness journey.
                    </p>
                </div>

                <div className="mt-8">
                    <button
                        onClick={handleGoogleLogin}
                        disabled={loading}
                        className="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150"
                    >
                        <svg className="h-5 w-5 mr-3" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                            <path d="M1 1h22v22H1z" fill="none"/>
                        </svg>
                        Sign in with Google
                    </button>
                </div>

                <div className="relative mt-6">
                    <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-500"></div></div>
                    <div className="relative flex justify-center text-sm"><span className="px-2 bg-[#023859] text-gray-400">Or continue with</span></div>
                </div>

                <form className="mt-6 space-y-6" onSubmit={handleLogin}>
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="username" className="sr-only">Username</label>
                            <input id="username" name="username" type="text" autoComplete="username" required placeholder="Your Username" value={username} onChange={(e) => setUsername(e.target.value)} className="appearance-none block w-full px-3 py-2 border bg-transparent border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"/>
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input id="password" name="password" type="password" autoComplete="current-password" required placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} className="appearance-none block w-full px-3 py-2 border bg-transparent border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"/>
                        </div>
                    </div>
                    {error && <div className="text-sm text-red-400 text-center bg-red-900 bg-opacity-30 p-2 rounded-md">{error}</div>}
                    <div className="flex items-center justify-end">
                        <div className="text-sm"><Link href="#" className="font-medium text-[#a7ebf2] hover:underline">Forgot your password?</Link></div>
                    </div>
                    <div>
                        <button type="submit" disabled={loading} className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-[#a7ebf2] bg-[#26658c] hover:bg-[#54acbf] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition disabled:opacity-50 disabled:cursor-not-allowed">
                            {loading ? 'Logging In...' : 'Log In'}
                        </button>
                    </div>
                </form>
                
                <div className="text-center mt-6">
                    <p className="text-sm text-[#91d7df]">Don&apos;t have an account?{' '}<Link href="/signup" className="font-medium text-[#a7ebf2] hover:underline">Sign up</Link></p>
                </div>
            </div>
        </div>
    );
}

