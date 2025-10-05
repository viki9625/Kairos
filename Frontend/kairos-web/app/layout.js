import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";
// --- THIS IS THE FIX ---
import { AuthProvider } from "@/app/context/AuthContext"; 

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata = {
    title: "Kairos",
    description: "Your Wellness Companion",
};

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
                <AuthProvider>
                    <Navbar />
                    <div className="min-h-[85.9vh]">
                        {children}
                    </div>
                    <Footer />
                </AuthProvider>
            </body>
        </html>
    );
}

