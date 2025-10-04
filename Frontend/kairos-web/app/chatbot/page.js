// app/chat/page.js (or wherever your chat component is located)

"use client";

import { useState, useEffect, useRef } from "react"; // Added useRef and useEffect for scrolling
import Image from "next/image";

// Mock history data for the sidebar menu
const mockChatHistoryList = [
  { id: 1, title: "Stress and Meditation" },
  { id: 2, title: "Goal Setting for Fitness" },
  { id: 3, title: "Understanding Anxiety" },
  { id: 4, title: "Sleep Routine Check" },
];

const initialChatHistory = [
  {
    sender: "Kairos",
    text: "Hello! I'm here to listen. How are you feeling today?",
  },
];

export default function Home() {
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState(initialChatHistory);
  const [isLoading, setIsLoading] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false); // NEW: State for the sidebar menu
  const messageEndRef = useRef(null); // Ref for auto-scrolling

  // Function to scroll to the latest message
  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages, isLoading]); // Scroll when messages update

  // Chat send handler
  const handleSend = async () => {
    if (chatInput.trim() === "" || isLoading) return;

    setIsLoading(true);
    const userMessage = { sender: "You", text: chatInput };
    setChatMessages((prev) => [...prev, userMessage]);
    setChatInput("");

    try {
      // NOTE: Original history mapping logic from your code is complex,
      // I'll leave the error handling but simplify the state updates.
      // You should adjust the history logic based on the actual API requirements.

      const historyToSend = [userMessage, ...chatMessages].map((msg) => ({
        role: msg.sender === "You" ? "user" : "assistant",
        parts: [{ text: msg.text }],
      }));

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: userMessage.text,
          history: historyToSend,
        }),
      });

      if (!response.ok) {
        // ... (Error handling remains the same)
        const KairosMessage = { sender: "Kairos", text: "Error: Could not connect to AI." };
        setChatMessages((prev) => [...prev, KairosMessage]);
        return;
      }

      const data = await response.json();
      const KairosMessage = { sender: "Kairos", text: data.text };
      setChatMessages((prev) => [...prev, KairosMessage]);
    } catch (error) {
      console.error("Frontend error:", error);
      const KairosMessage = { sender: "Kairos", text: "Sorry, a connection error occurred." };
      setChatMessages((prev) => [...prev, KairosMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Chat message bubble component
  const ChatMessage = ({ msg }) => {
    const isUser = msg.sender === "You";
    return (
      <div className={`mb-4 flex ${isUser ? "justify-end" : "justify-start"}`}>
        {!isUser && (
          <div className="w-8 h-8 rounded-full mr-2 flex-shrink-0">
            <Image
              src="/chatbot_logo.svg"
              alt="Kairos Avatar"
              width={32}
              height={32}
            />
          </div>
        )}

        <div
          className={`px-3 py-2 max-w-[75%] rounded-xl text-sm break-words ${
            isUser
              ? "bg-[#54acbf] text-white rounded-tr-none"
              : "bg-[#a7ebf2] text-[#023859] rounded-tl-none"
          }`}
        >
          <span className="leading-relaxed flex-shrink-0 whitespace-pre-wrap">{msg.text}</span>
        </div>
        
        {isUser && (
          <div className="w-8 h-8 rounded-full ml-2 flex-shrink-0">
            <Image
              src="/user.png"
              alt="You Avatar"
              width={32}
              height={32}
              className="filter invert"
            />
          </div>
        )}
      </div>
    );
  };
  
  return (
    // Outer container (full height and background)
    <div className="bg-[#a7ebf2] min-h-[84.5vh] flex flex-col p-4 relative overflow-hidden">
      <main className="flex-1 flex flex-col md:flex-row gap-4">
        {/* Chat Interface Container */}
        <div className="relative flex-1 flex flex-col bg-[#023859] rounded-lg shadow-xl overflow-hidden">
          
          
          {/* Header/Chat Info */}
          <div className="flex items-center justify-between px-4 py-3 border-b-2 border-gray-700 flex-shrink-0 ">
            <div className="flex items-center">
              <div className="rounded-full mr-4 w-10 h-10">
                <Image
                  src="/chatbot_logo.svg"
                  alt="Kairos"
                  width={40} 
                  height={40} 
                />
              </div>
              <div>
                <p className="font-semibold text-[#a7ebf2]">Kairos</p>
                <p className="text-xs text-gray-400">Your wellness companion</p>
              </div>
            </div>
            
            {/* Hamburger/Menu Toggle Button (UPDATED) */}
            <button 
              className="text-[#a7ebf2] hover:text-white p-1 transition-colors " 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle chat history menu"
            >
              {isMenuOpen ? ( // 👈 Conditional Rendering based on state
                // X Icon (Close)
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
                // Hamburger Icon (Open)
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
          </div>
          
          {/* Sliding Chat History Sidebar (NEW) */}
          <div 
            className={`
              absolute top-0 right-0 h-full w-full md:w-80 bg-[#011c40] shadow-2xl z-20 
              transform transition-transform duration-300 ease-in-out
              ${isMenuOpen ? 'translate-x-0' : 'translate-x-full'}
            `}
          >
            <div> {/* Add padding for space below main header */}
                <div className="flex items-center justify-between mb-4 p-4 pt-6 text-lg font-bold text-[#a7ebf2]  border-b border-gray-700 pb-2">

                
              <h3>
                Previous Chats
              </h3>
              <button 
              className="text-[#a7ebf2] hover:text-white p-1 transition-colors " 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle chat history menu"
            >
              {isMenuOpen ? ( // 👈 Conditional Rendering based on state
                // X Icon (Close)
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
              )
              :(
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
              )}
            </button>
            </div>
              <ul className="space-y-2">
                {mockChatHistoryList.map((chat) => (
                  <li 
                    key={chat.id} 
                    className="text-sm text-gray-300 p-2 rounded-lg hover:bg-[#023859] cursor-pointer transition-colors truncate"
                  >
                    {chat.title}
                  </li>
                ))}
              </ul>
             
            </div>
          </div>


          {/* Chat Messages Display Area */}
          <div
            className="flex-1 p-4 overflow-y-auto hide-scrollbar"
            style={{ height: "calc(100vh - 240px)" }}
          >
            <div className="max-w-4xl mx-auto space-y-4"> {/* Added space-y-4 for consistent spacing */}
              {chatMessages.map((msg, idx) => (
                <ChatMessage key={idx} msg={msg} />
              ))}
              {/* Kairos is typing indicator */}
              {isLoading && (
                <div className="flex items-start">
                  <div className="w-8 h-8 rounded-full mr-2 flex-shrink-0">
                    <Image
                      src="/chatbot_logo.svg"
                      alt="Kairos"
                      width={32}
                      height={32}
                    />
                  </div>
                  <div className="rounded-xl p-3 max-w-[80%] text-[#a7ebf2] animate-pulse">
                    <span className="text-sm">Kairos is typing...</span>
                  </div>
                </div>
              )}
              <div ref={messageEndRef} />
            </div>
          </div>
          
          {/* Input Bar */}
          <div className="p-4 border-t-2 border-gray-700 flex-shrink-0">
            <div className="max-w-4xl mx-auto flex gap-2">
              <input
                type="text"
                className="flex-1 border-0 rounded-full px-4 py-3 bg-gray-600/50 text-white placeholder-gray-400 focus:ring-2 focus:ring-[#a7ebf2] focus:border-transparent outline-none transition-colors"
                placeholder="Type your message..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSend();
                }}
              />
              <button
                className={`
                  p-3 rounded-full hover:bg-[#01295c] transition-colors flex items-center justify-center flex-shrink-0
                  ${isLoading ? 'bg-[#011c40] opacity-50 cursor-not-allowed' : 'bg-[#011c40] cursor-pointer'}
                `}
                onClick={handleSend}
                disabled={isLoading}
              >
                <Image src="/send.svg" alt="Send" width={20} height={20}/>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}