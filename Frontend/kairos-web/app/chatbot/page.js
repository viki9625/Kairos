"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useAuth } from "@/app/context/AuthContext";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const WS_URL = process.env.NEXT_PUBLIC_WS_URL;	

// --- Reusable SVG Icons ---
const MenuIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg> );
const CloseIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg> );
const PlusIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg> );
const LogoutIcon = () => ( <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg> );

export default function ChatbotPage() {
    // --- Simplified State ---
    const [chatInput, setChatInput] = useState("");
    const [chatMessages, setChatMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    
    const { user, loading: authLoading, logout } = useAuth();
    const websocket = useRef(null);
    const messageEndRef = useRef(null);
    const router = useRouter();
    const userId = user?.userId;

    // 1. Protect the route
    useEffect(() => {
        if (!authLoading && !user) {
            router.push("/login");
        }
    }, [user, authLoading, router]);

    // 2. Fetch the user's ENTIRE chat history
    useEffect(() => {
        if (!userId) return;

        const fetchHistory = async () => {
            setIsLoading(true);
            try {
                // Calls the correct, simpler history endpoint
                const response = await fetch(`${API_URL}/api/chat/history/${userId}`);
                if (response.ok) {
                    const history = await response.json();
                    const formatted = history.map(msg => ({ sender: msg.role === 'user' ? 'You' : 'Kairos', text: msg.content }));
                    setChatMessages(formatted.length > 0 ? formatted : [{ sender: "Kairos", text: "Welcome! How can I help?" }]);
                } else {
                   setChatMessages([{ sender: "Kairos", text: "Welcome! How can I help?" }]);
                }
            } catch (error) {
                setChatMessages([{ sender: "Kairos", text: "Error connecting. Please refresh." }]);
            } finally {
                setIsLoading(false);
            }
        };
        fetchHistory();
    }, [userId]);

    // 3. Connect to the WebSocket
    useEffect(() => {
        if (!userId) return;
        const ws = new WebSocket(`${WS_URL}/api/chat/ws/${userId}`);
        ws.onopen = () => console.log("WebSocket established");
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setChatMessages((prev) => [...prev, { sender: 'Kairos', text: message.content }]);
        };
        ws.onerror = (error) => console.error("WebSocket error:", error);
        ws.onclose = () => console.log("WebSocket closed");
        websocket.current = ws;
        return () => { if (websocket.current) websocket.current.close(); };
    }, [userId]);

    // 4. Auto-scroll to the bottom of the chat
    useEffect(() => {
        messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatMessages]);

    // --- HANDLER FUNCTIONS ---
    
    // Simplified send handler (no conversation_id)
    const handleSend = () => {
        if (!chatInput.trim() || !websocket.current || websocket.current.readyState !== WebSocket.OPEN) return;
        
        websocket.current.send(JSON.stringify({ message: chatInput }));
        
        const userMessage = { sender: "You", text: chatInput };
        setChatMessages((prev) => [...prev, userMessage]);
        setChatInput("");
    };

    // "New Chat" button now just clears the current messages from view
    const handleNewChat = () => {
        setChatMessages([{ sender: "Kairos", text: "Of course. What's on your mind now?" }]);
        setIsSidebarOpen(false);
    };

    const handleLogout = () => {
        logout();
        router.push('/login');
    };
    
    // Loading spinner while checking authentication
    if (authLoading || !user) {
        return (
             <div className="bg-[#a7ebf2] w-full min-h-[84.5vh] flex items-center justify-center">
                <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-[#023859]"></div>
             </div>
        );
    }

    return (
        <div className="bg-[#a7ebf2] h-[84.5vh] flex flex-col relative overflow-hidden p-4">
            {/* --- Sidebar --- */}
            <aside className={`absolute top-0 left-0 h-full bg-[#011c40] w-64 md:w-80 shadow-2xl z-30 transform transition-transform duration-300 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="p-4 flex flex-col h-full">
                    <div className="flex justify-between items-center mb-4 flex-shrink-0">
                        <h2 className="text-xl font-bold text-[#a7ebf2]">Chat History</h2>
                        <button onClick={() => setIsSidebarOpen(false)} className="text-[#a7ebf2] p-1 rounded-full hover:bg-white/10"><CloseIcon/></button>
                    </div>
                    <button onClick={handleNewChat} className="flex items-center justify-center w-full p-2 mb-4 text-[#a7ebf2] bg-white/5 rounded-md hover:bg-white/10"><PlusIcon /> <span className="ml-2">New Chat</span></button>
                    
                    {/* MODIFIED: Renders the simple list of all messages */}
                    <ul className="space-y-2 overflow-y-auto flex-1">
                       {chatMessages.map((msg, idx) => (
                           <li key={idx} className={`p-2 rounded-md text-sm truncate ${msg.sender === 'You' ? 'text-gray-400 text-right' : 'text-gray-200'}`}>{msg.text}</li>
                       ))}
                    </ul>

                    <div className="mt-4 flex-shrink-0">
                         <button onClick={handleLogout} className="flex items-center w-full p-2 text-red-400 hover:bg-red-500/10 rounded-md"><LogoutIcon /> <span className="ml-2">Log Out</span></button>
                    </div>
                </div>
            </aside>

            {/* --- Main Chat Window --- */}
            <main className="flex-1 flex flex-col min-h-0">
                 <div className="relative flex-1 flex flex-col bg-[#023859] rounded-lg shadow-xl overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-3 border-b-2 border-gray-700 flex-shrink-0">
                        <div className="flex items-center">
                             <button onClick={() => setIsSidebarOpen(true)} className="mr-4 text-[#a7ebf2] p-2 rounded-full hover:bg-white/10"><MenuIcon /></button>
                             <div className="rounded-full mr-4 w-10 h-10"><Image src="/chatbot_logo.svg" alt="Kairos" width={40} height={40}/></div>
                             <div>
                                 <p className="font-semibold text-[#a7ebf2]">Kairos</p>
                                 <p className="text-xs text-gray-400">Your wellness companion</p>
                             </div>
                        </div>
                    </div>
                    <div className="flex-1 p-4 overflow-y-auto">
                        <div className="max-w-4xl mx-auto w-full">
                            {isLoading ? (
                                <div className="flex justify-center items-center h-full"><div className="w-8 h-8 border-4 border-dashed rounded-full animate-spin border-[#a7ebf2]"></div></div>
                            ) : (
                                chatMessages.map((msg, idx) => <ChatMessageBubble key={idx} msg={msg} />)
                            )}
                            <div ref={messageEndRef} />
                        </div>
                    </div>
                    <div className="p-4 border-t-2 border-gray-700 flex-shrink-0">
                        <div className="max-w-4xl mx-auto flex gap-2">
                            <input type="text" className="flex-1 border-0 rounded-full px-4 py-3 bg-gray-600/50 text-white placeholder-gray-400 focus:ring-2 focus:ring-[#a7ebf2] outline-none" placeholder="Type your message..." value={chatInput} onChange={(e) => setChatInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") handleSend(); }}/>
                            <button className="p-3 rounded-full hover:bg-[#01295c] bg-[#011c40] cursor-pointer" onClick={handleSend}><Image src="/send.svg" alt="Send" width={20} height={20} /></button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

// Reusable ChatMessageBubble component
const ChatMessageBubble = ({ msg }) => {
    const isUser = msg.sender === "You";
    return (
        <div className={`mb-4 flex ${isUser ? "justify-end" : "justify-start"}`}>
            {!isUser && <div className="w-8 h-8 flex-shrink-0"><Image src="/chatbot_logo.svg" alt="Kairos" width={32} height={32} /></div>}
            <div className={`px-4 py-2 max-w-[80%] rounded-2xl text-base break-words mx-2 shadow-md ${ isUser ? "bg-[#54acbf] text-white rounded-tr-none" : "bg-[#a7ebf2] text-[#023859] rounded-tl-none"}`}>
                <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
            </div>
            {isUser && <div className="w-8 h-8 flex-shrink-0"><Image src="/user.png" alt="You" width={32} height={32} className="filter invert" /></div>}
        </div>
    );
};

