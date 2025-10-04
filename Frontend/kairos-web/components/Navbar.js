// components/Navbar.js

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";
import { useState } from "react";

export default function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  // Define all possible links
  const links = [
    { href: "/", label: "Home", type: "nav" },
    { href: "/login", label: "Login", type: "action" },
    { href: "/signup", label: "Signup", type: "action" },
    { href: "/about", label: "About", type: "info" },
    { href: "/chatbot", label: "Indicator", type: "indicator" },
  ];

  const getDisplayLinks = () => {
    const aboutLink = links.find((link) => link.href === "/about");
    const homeLink = links.find((link) => link.href === "/");
    const loginLink = links.find((link) => link.href === "/login");
    const signupLink = links.find((link) => link.href === "/signup");

    switch (pathname) {
      case "/login":
        return [aboutLink, homeLink, signupLink].filter(Boolean);
        
      case "/signup":
        return [aboutLink, homeLink, loginLink].filter(Boolean);
        
      case "/chatbot": 
        // For chatbot, we only need the About link in the desktop view (indicator is handled separately)
        return [aboutLink].filter(Boolean); 

      case "/about":
        return [homeLink, loginLink, signupLink].filter(Boolean);

      case "/":
      default:
        return [aboutLink, loginLink, signupLink].filter(Boolean);
    }
  };

  const displayLinks = getDisplayLinks();
  
  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const getButtonStyles = (link) => {
    // 1. Styling for the About link (Text link, desktop & mobile)
    if (link.href === "/about") {
      return "text-[#a7ebf2] hover:text-white font-semibold";
    }
    
    // 2. Styling for Login/Signup/Home buttons (Desktop buttons)
    return pathname === link.href
      ? "bg-[#316a8d] text-white shadow-lg" // Active style
      : "bg-[#26658c] text-[#a7ebf2] hover:bg-[#418dbd]"; // Inactive style
  };

  // Styles for mobile menu links (simple text links)
  const getMobileLinkStyles = (link) => {
    return link.href === pathname
        ? "text-white bg-white/10" // Highlight active link
        : "text-[#a7ebf2] hover:bg-white/10";
  }
  
  // Custom indicator styling (pulled out for separate rendering)
  const indicatorStyles = "w-10 h-10 rounded-full bg-white border-2 border-[#a7ebf2] flex-shrink-0";
  const isChatbotPage = pathname === "/chatbot";

  return (
    <nav className="bg-[#011c40] p-4 shadow-md">
      <div className="mx-auto flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="z-20" onClick={() => setIsOpen(false)}>
          <div className="flex items-center gap-2 text-[#a7ebf2] text-2xl font-bold tracking-wider">
            <Image src={"/logo.svg"} width={36} height={36} alt="KAIROS logo" />
            <div>KAIROS</div>
          </div>
        </Link>

        {/* --- Navigation Controls Area --- */}
        <div className="flex items-center gap-4">
          
          {/* 1. Mobile Indicator (Only on Chatbot page, Mobile) */}
          {isChatbotPage && (
            <div className={`md:hidden ${indicatorStyles} order-first`}>
              {/* Optional: User initials or image inside */}
            </div>
          )}

          {/* 2. Mobile Hamburger Button */}
          <button
            className={`md:hidden text-[#a7ebf2] p-2 z-20 ${isChatbotPage ? 'order-last' : ''}`}
            onClick={toggleMenu}
            aria-label="Toggle navigation menu"
          >
            {isOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
            )}
          </button>
          
          {/* 3. Desktop Navigation Links (including About and conditional buttons) */}
          <div className="hidden md:flex space-x-4 items-center">
            {displayLinks.map((link) => (
              // The indicator is now NOT mapped here
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`
                  px-4 py-2 rounded-full font-medium transition duration-150 ease-in-out
                  ${getButtonStyles(link)}
                `}
              >
                {link.label}
              </Link>
            ))}
            
            {/* 4. Desktop Indicator (Only on Chatbot page, Desktop) */}
            {isChatbotPage && (
                <div 
                    key="desktop-indicator"
                    className={indicatorStyles} 
                    title="User Profile" 
                ></div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown (INSTANT TOGGLE, h=10vh) */}
      <div
        className={`
          md:hidden absolute top-16 left-0 w-full min-h-[5vh] bg-[#011c40] p-1 border-t border-gray-700
          ${isOpen ? "block z-10" : "hidden"}
        `}
      >
        <ul className="h-full overflow-y-auto space-y-1">
          {displayLinks
            // The indicator link is never added to the mobile dropdown list
            .map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`
                  w-full block text-left px-4 py-1 text-sm font-semibold transition duration-150 ease-in-out
                  ${getMobileLinkStyles(link)}
                `}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}