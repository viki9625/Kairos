'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const handleSignup = async (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    anonymous: false,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('userId', data.user_id);
                router.push('/chatbot');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Failed to sign up. Please try again.');
            }
        } catch (err) {
            setError('An error occurred. Please try again later.');
            console.error('Signup error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = () => {
        // This function is identical to the one on the login page.
        // It redirects to the same backend endpoint, which handles both login and signup.
        window.location.href = `${API_URL}/api/auth/google/login`;
    };

    return (
        <div className="min-h-[85.9vh] bg-[#a7ebf2] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full bg-[#023859] p-8 md:p-10 rounded-xl shadow-2xl">
                
                <div>
                    <h2 className="text-center text-3xl font-extrabold text-[#a7ebf2]">
                        Create your account
                    </h2>
                    <p className="mt-2 text-center text-sm text-[#aff7ff]">
                        Join us and start your wellness journey.
                    </p>
                </div>

                {/* --- Sign Up with Google Button --- */}
                <div className="mt-8">
                    <button
                        onClick={handleGoogleLogin}
                        disabled={loading}
                        className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150"
                    >
                        <svg className="h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24px" height="24px"><path fill="#fbc02d" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12 s5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24s8.955,20,20,20  s20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"></path><path fill="#e53935" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039 l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"></path><path fill="#4caf50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36 c-5.222,0-9.519-3.487-11.187-8.264l-6.522,5.025C9.505,39.556,16.227,44,24,44z"></path><path fill="#1565c0" d="M43.611,20.083L43.595,20L42,20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.574 l6.19,5.238C39.971,36.216,44,30.563,44,24C44,22.659,43.862,21.35,43.611,20.083z"></path></svg>
                        Sign up with Google
                    </button>
                </div>

                <div className="relative mt-6">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-gray-500"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                        <span className="px-2 bg-[#023859] text-gray-400">Or continue with</span>
                    </div>
                </div>

                <form className="mt-6 space-y-6" onSubmit={handleSignup}>
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="username" className="sr-only">Username</label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                required
                                placeholder="Enter a username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="appearance-none relative block w-full px-3 py-2 border bg-transparent border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="appearance-none relative block w-full px-3 py-2 border bg-transparent border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
                            />
                        </div>
                         <div>
                            <label htmlFor="confirm-password" className="sr-only">Confirm Password</label>
                            <input
                                id="confirm-password"
                                name="confirm-password"
                                type="password"
                                required
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="appearance-none relative block w-full px-3 py-2 border bg-transparent border-gray-300 placeholder-[#91d7df] text-white rounded-md focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm"
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="text-sm text-red-400 text-center bg-red-900 bg-opacity-30 p-2 rounded-md">
                            {error}
                        </div>
                    )}

                    <div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-[#a7ebf2] bg-[#26658c] hover:bg-[#54acbf] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Creating Account...' : 'Sign Up'}
                        </button>
                    </div>
                </form>
                
                <div className="text-center mt-6">
                    <p className="text-sm text-[#91d7df]">
                        Already have an account?{' '}
                        <Link href="/login" className="font-medium text-[#a7ebf2] hover:underline">
                            Log in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

