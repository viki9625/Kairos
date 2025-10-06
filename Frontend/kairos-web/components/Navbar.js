"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import { useAuth } from "@/app/context/AuthContext";

// (SVG Icons remain the same)
const LogoutIcon = () => ( <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg> );
const CloseIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg> );
const MenuIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg> );

export default function Navbar() {
    const pathname = usePathname();
    const router = useRouter();
    const { user, logout } = useAuth();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [userDetails, setUserDetails] = useState(null);
    const profileRef = useRef(null);
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    useEffect(() => {
        if (user?.token) {
            const fetchUserDetails = async () => {
                try {
                    const response = await fetch(`${API_URL}/api/users/me`, {
                        headers: { 'Authorization': `Bearer ${user.token}` }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        setUserDetails(data);
                    } else {
                        console.error("Failed to fetch user details");
                    }
                } catch (error) {
                    console.error("Error fetching user details:", error);
                }
            };
            fetchUserDetails();
        } else {
            setUserDetails(null);
        }
    }, [user]);

    useEffect(() => {
        function handleClickOutside(event) {
            if (profileRef.current && !profileRef.current.contains(event.target)) {
                setIsProfileOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [profileRef]);

    const handleLogout = () => {
        // --- DEBUGGING: Checkpoint 1 ---
        console.log("Navbar: handleLogout function started.");
        
        try {
            logout();
            // --- DEBUGGING: Checkpoint 2 ---
            console.log("Navbar: logout() from context was called.");
            
            setIsProfileOpen(false);
            setIsMobileMenuOpen(false);
            
            // --- DEBUGGING: Checkpoint 3 ---
            console.log("Navbar: Attempting to redirect to /login");
            router.push('/login');
            
            // --- DEBUGGING: Checkpoint 4 ---
            console.log("Navbar: Redirect command was issued.");

        } catch (error) {
            // --- DEBUGGING: Checkpoint 5 (Crucial!) ---
            console.error("A critical error occurred inside handleLogout:", error);
        }
    };

    // (The rest of your JSX and functions remain the same)
    const getDisplayLinks = () => {
        const aboutLink = { href: "/about", label: "About" };
        const homeLink = { href: "/", label: "Home" };
        const loginLink = { href: "/login", label: "Login" };
        const signupLink = { href: "/signup", label: "Signup" };
        if (user) {
            switch (pathname) {
                case "/chatbot": return [aboutLink];
                case "/about": return [homeLink];
                default: return [aboutLink];
            }
        }
        switch (pathname) {
            case "/login": return [aboutLink, homeLink, signupLink];
            case "/signup": return [aboutLink, homeLink, loginLink];
            case "/about": return [homeLink, loginLink, signupLink];
            default: return [aboutLink, loginLink, signupLink];
        }
    };
    const displayLinks = getDisplayLinks();
    const getButtonStyles = (link) => {
        if (link.href === "/about") return "text-[#a7ebf2] hover:text-white font-semibold";
        return pathname === link.href ? "bg-[#316a8d] text-white shadow-lg" : "bg-[#26658c] text-[#a7ebf2] hover:bg-[#418dbd]";
    };
    const getMobileLinkStyles = (link) => {
        return pathname === link.href ? "text-white bg-white/10" : "text-[#a7ebf2] hover:bg-white/10";
    };
    const isChatbotPage = pathname === "/chatbot";

    return (
        <nav className="bg-[#011c40] p-4 shadow-md relative z-40">
            <div className="mx-auto flex justify-between items-center">
                <Link href="/" className="z-20 flex items-center gap-3 text-[#a7ebf2] text-2xl font-bold tracking-wider whitespace-nowrap" onClick={() => setIsMobileMenuOpen(false)}>
                    <Image src={"/logo.png"} width={40} height={40} alt="KAIROS logo" suppressHydrationWarning={true}/>
                    <div>KAIROS</div>
                </Link>
                <div className="flex items-center gap-4">
                    {user && isChatbotPage && (
                        <div className="md:hidden order-first" ref={profileRef}>
                            <button onClick={() => setIsProfileOpen(!isProfileOpen)} className="w-10 h-10 rounded-full border-2 border-[#a7ebf2] overflow-hidden bg-gray-600">
                                <Image src={userDetails?.profile_picture_url || '/user.png'} alt="Profile" width={40} height={40} className={!userDetails?.profile_picture_url ? "filter invert p-1" : "object-cover w-full h-full"} unoptimized/>
                            </button>
                        </div>
                    )}
                    <button className={`md:hidden text-[#a7ebf2] p-2 z-20 ${isChatbotPage && user ? 'order-last' : ''}`} onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} aria-label="Toggle navigation menu">
                        {isMobileMenuOpen ? <CloseIcon/> : <MenuIcon />}
                    </button>
                    <div className="hidden md:flex space-x-4 items-center">
                        {displayLinks.map((link) => (
                            <Link key={link.href} href={link.href} className={`px-4 py-2 rounded-full font-medium transition duration-150 ease-in-out ${getButtonStyles(link)}`}>
                                {link.label}
                            </Link>
                        ))}
                        {user && (
                            <div className="relative" ref={profileRef}>
                                <button onClick={() => setIsProfileOpen(!isProfileOpen)} className="w-10 h-10 rounded-full border-2 border-[#a7ebf2] flex-shrink-0 overflow-hidden bg-gray-600">
                                    <Image src={userDetails?.profile_picture_url || '/user.png'} alt="User Profile" width={40} height={40} className={!userDetails?.profile_picture_url ? "filter invert p-1" : "object-cover w-full h-full"} unoptimized/>
                                </button>
                                {isProfileOpen && (
                                    <div className="absolute right-0 mt-2 w-72 bg-[#023859] rounded-lg shadow-xl border border-gray-700 py-2">
                                        <div className="px-4 py-3 border-b border-gray-700">
                                            <p className="font-bold text-white truncate">{userDetails?.username || 'Wellness User'}</p>
                                            <p className="text-sm text-gray-400 truncate">{userDetails?.email || `User ID: ${user.userId}`}</p>
                                        </div>
                                        <div className="mt-2 px-2">
                                            <button onClick={handleLogout} className="flex items-center w-full text-left px-3 py-2 text-red-400 hover:bg-red-500/10 rounded-md transition-colors">
                                                <LogoutIcon />
                                                <span>Log Out</span>
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
            {isMobileMenuOpen && (
                <div className="md:hidden absolute top-16 left-0 w-full bg-[#011c40] p-4 border-t border-gray-700">
                    <ul className="space-y-2">
                        {displayLinks.map((link) => (
                            <li key={link.href}>
                                <Link href={link.href} onClick={() => setIsMobileMenuOpen(false)} className={`w-full block text-left px-4 py-2 text-lg font-semibold rounded-md ${getMobileLinkStyles(link)}`}>
                                    {link.label}
                                </Link>
                            </li>
                        ))}
                        {user && (
                           <li><button onClick={handleLogout} className="flex items-center w-full text-left px-4 py-2 text-lg font-semibold text-red-400 hover:bg-red-500/10 rounded-md"><LogoutIcon /> Log Out</button></li>
                        )}
                    </ul>
                </div>
            )}
        </nav>
    );
}

