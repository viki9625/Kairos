'use client';

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/app/context/AuthContext';

export default function CallbackHandler() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const { setUser } = useAuth();

    useEffect(() => {
        // This logic reads the token and user_id from the URL.
        const token = searchParams.get('token');
        const userId = searchParams.get('user_id');

        if (token && userId) {
            // If found, save them to local storage.
            localStorage.setItem('accessToken', token);
            localStorage.setItem('userId', userId);

            // Directly update the global auth state
            setUser({ token, userId });
            
            // Redirect to the chatbot page.
            router.push('/chatbot');
        } else {
            // If not found, something went wrong. Go back to login.
            console.error("Google login callback is missing token or user_id.");
            router.push('/login');
        }
    }, [router, searchParams, setUser]);

    // The loading message is now part of this client component.
    return (
        <div className="text-center">
            <p className="text-xl font-semibold text-[#023859]">
                Finalizing your login, please wait...
            </p>
            <div className="mt-4 w-12 h-12 border-4 border-dashed rounded-full animate-spin border-[#023859]"></div>
        </div>
    );
}

