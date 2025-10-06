'use client';

import Link from "next/link";
import Image from "next/image";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/app/context/AuthContext"; // Corrected import path

// A simple component to show while we check the user's login status
const LoadingSpinner = () => (
    <div className="flex justify-center items-center h-full">
        <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-[#023859]"></div>
    </div>
);

// SVG Icon for the buttons (remains the same)
const ArrowRightIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
    </svg>
);


export default function WelcomePage() {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        // This effect runs when the component loads
        // 'loading' will be true initially, then false after checking localStorage
        if (!loading && user) {
            // If we are done loading and a user exists, redirect them
            router.push('/chatbot'); 
        }
    }, [user, loading, router]);

    // While we are checking for a user, or if we found one and are redirecting,
    // show a loading spinner to prevent the welcome page from flashing.
    if (loading || user) {
        return (
             <div className="bg-gradient-to-br from-[#a7ebf2] to-[#89d8e0] min-h-[85.9vh] flex items-center justify-center">
                <LoadingSpinner />
             </div>
        );
    }
    
    // If we are done loading and there is NO user, show the normal welcome page.
    return (
        <div className="bg-gradient-to-br from-[#a7ebf2] to-[#89d8e0] min-h-[86.4vh] flex items-center justify-center overflow-hidden">
            <div className="container mx-auto px-6 py-16">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
                    <div className="text-center md:text-left animate-fade-in-up">
                        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-[#011c40] leading-tight mb-6">
                            Your Personal Wellness Companion
                        </h1>
                        <p className="text-lg md:text-xl text-[#023859] max-w-prose mx-auto md:mx-0 mb-8">
                            Begin your journey to a healthier, happier you. Kairos offers
                            personalized support for both your mental and physical well-being.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                            <Link href={"/signup"}>
                                <button className="group flex items-center justify-center w-full sm:w-auto bg-[#26658c] text-white px-8 py-3 rounded-full font-bold text-lg shadow-lg hover:bg-[#317ca8] transform hover:scale-105 transition-all duration-300">
                                    <span>Get Started</span>
                                    <ArrowRightIcon />
                                </button>
                            </Link>
                            <Link href={"/login"}>
                                <button className="group flex items-center justify-center w-full sm:w-auto bg-transparent border-2 border-[#26658c] text-[#023859] px-8 py-3 rounded-full font-bold text-lg shadow-lg hover:bg-[#26658c] hover:text-white transform hover:scale-105 transition-all duration-300">
                                    <span>Log In</span>
                                </button>
                            </Link>
                        </div>
                    </div>
                    <div className="hidden md:flex justify-center items-center animate-fade-in-up animation-delay-300">
                        <svg width="100%" height="100%" viewBox="0 0 400 400" className="max-w-md">
                            <defs>
                                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style={{stopColor: '#54acbf', stopOpacity: 1}} />
                                    <stop offset="100%" style={{stopColor: '#26658c', stopOpacity: 1}} />
                                </linearGradient>
                            </defs>
                            <path 
                                fill="url(#grad1)"
                                d="M369.5,236.25Q347,272.5,310.25,291.75Q273.5,311,236.75,321Q200,331,165.5,318.25Q131,305.5,102.5,283Q74,260.5,56,230.25Q38,200,60.5,168.25Q83,136.5,103.5,111.5Q124,86.5,162,75.75Q200,65,234.5,75.5Q269,86,298,109.25Q327,132.5,353,166.25Q379,200,369.5,236.25Z"
                            />
                            <circle cx="120" cy="150" r="15" fill="#a7ebf2" className="opacity-70 animate-pulse" />
                            <circle cx="280" cy="250" r="25" fill="#a7ebf2" className="opacity-60 animate-pulse animation-delay-500" />
                             <circle cx="290" cy="120" r="10" fill="#ffffff" className="opacity-80 animate-pulse animation-delay-200" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    );
}

