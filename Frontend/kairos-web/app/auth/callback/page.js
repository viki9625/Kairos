'use client';

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function AuthCallbackPage() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const token = searchParams.get('token');
        // --- THIS IS THE FIX ---
        // The variable was 'search_params' but should be 'searchParams'
        const userId = searchParams.get('user_id'); 
        // ----------------------

        if (token && userId) {
            // If the token and user ID are found, save them.
            localStorage.setItem('accessToken', token);
            localStorage.setItem('userId', userId);
            
            // Redirect to the chatbot page.
            router.push('/chatbot');
        } else {
            // If something is missing, send the user back to the login page.
            console.error("Google login callback is missing token or user_id.");
            router.push('/login');
        }
    }, [router, searchParams]);

    // Display a loading message while processing.
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

