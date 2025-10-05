'use client';

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/app/context/AuthContext'; // <-- Import the useAuth hook

export default function AuthCallbackPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const { setUser } = useAuth(); // <-- Get the setUser function from our global context

    useEffect(() => {
        const token = searchParams.get('token');
        const userId = searchParams.get('user_id');

        if (token && userId) {
            // Save the credentials to local storage
            localStorage.setItem('accessToken', token);
            localStorage.setItem('userId', userId);
            
            // --- THIS IS THE FIX ---
            // Directly update the global authentication state.
            // This prevents the race condition on the next page.
            setUser({ token, userId });
            // ----------------------
            
            // Now, redirect the user to the chatbot page
            router.push('/chatbot');
        } else {
            // If something is wrong, go back to the login page
            console.error("Google login callback is missing token or user_id.");
            router.push('/login');
        }
    }, [router, searchParams, setUser]); // Add setUser to the dependency array

    // Display a loading message while the redirect is processed
    return (
        <div className="min-h-[84.5vh] bg-[#a7ebf2] flex items-center justify-center">
            <div className="text-center">
                <p className="text-xl font-semibold text-[#023859]">
                    Finalizing your login, please wait...
                </p>
                <div className="mt-4 w-12 h-12 border-4 border-dashed rounded-full animate-spin border-[#023859]"></div>
            </div>
        </div>
    );
}

