"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";
import { useState } from "react";

export default function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const links = [
    { href: "/", label: "Home", type: "nav" },
    { href: "/login", label: "Login", type: "action" },
    { href: "/signup", label: "Signup", type: "action" },
    { href: "/about", label: "About", type: "info" },
  ];

  const getDisplayLinks = () => {
    let conditionalLinks;
    switch (pathname) {
      case "/login":
        conditionalLinks = links.filter(
          (link) => link.href === "/" || link.href === "/signup"
        );
        break;
      case "/signup":
        conditionalLinks = links.filter(
          (link) => link.href === "/" || link.href === "/login"
        );
        break;
      case "/":
      default:
        conditionalLinks = links.filter(
          (link) => link.href === "/login" || link.href === "/signup"
        );
        break;
    }

    const aboutLink = links.find((link) => link.href === "/about");
    if (pathname === "/about") {
      return conditionalLinks;
    } else {
      return [aboutLink, ...conditionalLinks].filter(Boolean);
    }
  };

  const displayLinks = getDisplayLinks();
  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const getButtonStyles = (link) => {
    return link.href === "/about"
      ? "text-[#a7ebf2] hover:text-white font-semibold"
      : pathname === link.href
      ? "bg-[#316a8d] text-white shadow-lg"
      : "bg-[#26658c] text-[#a7ebf2] hover:bg-[#418dbd]";
  };

  return (
    <nav className="bg-[#011c40] p-4 shadow-md">
      <div className="mx-auto flex justify-between items-center">
        <Link href="/" className="z-20" onClick={() => setIsOpen(false)}>
          <div className="flex items-center gap-2 text-[#a7ebf2] text-2xl font-bold tracking-wider">
            <Image src={"/logo.svg"} width={36} height={36} alt="KAIROS logo" />
            <div>KAIROS</div>
          </div>
        </Link>

        <button
          className="md:hidden text-[#a7ebf2] p-2 z-20"
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
        >
          {isOpen ? (
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          ) : (
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16m-7 6h7"
              ></path>
            </svg>
          )}
        </button>

        <div className="hidden md:flex space-x-4">
          {displayLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`
                px-4 py-2 rounded-full font-medium transition duration-150 ease-in-out
                ${getButtonStyles(link)}
              `}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      <div
        className={`
          md:hidden absolute top-0 left-0 w-full h-screen bg-[#011c40] p-8 space-y-4
          transition-transform duration-300 ease-in-out transform
          ${isOpen ? "translate-x-0 z-10" : "translate-x-full"}
        `}
      >
        <div className="mt-20 flex flex-col items-center space-y-6">
          {displayLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setIsOpen(false)}
              className={`
                w-full text-center px-6 py-3 rounded-full text-lg font-semibold transition duration-150 ease-in-out
                ${
                  link.href === "/about"
                    ? "text-[#a7ebf2] hover:bg-white/10"
                    : "bg-[#26658c] text-[#a7ebf2] hover:bg-[#418dbd]"
                }
              `}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
