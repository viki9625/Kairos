"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

// Define the URLs for your FastAPI backend
const API_URL = process.env.NEXT_PUBLIC_API_URL;
const WS_URL = process.env.NEXT_PUBLIC_WS_URL;

export default function ChatbotPage() {
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false); // Used for initial history load
  const [userId, setUserId] = useState(null);
  const websocket = useRef(null);
  const messageEndRef = useRef(null);
  const router = useRouter();

  // --- 1. Protect the Route and Get User ID ---
  useEffect(() => {
    const storedUserId = localStorage.getItem("userId");
    const token = localStorage.getItem("accessToken");

    if (!storedUserId || !token) {
      router.push("/login"); // Redirect if not logged in
    } else {
      setUserId(storedUserId);
    }
  }, [router]);

  // --- 2. Fetch Chat History ---
  useEffect(() => {
    if (!userId) return; // Don't fetch until we have a user ID

    const fetchHistory = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/api/chat/history/${userId}`);
        if (response.ok) {
          const history = await response.json();
          // Format the history to match the component's expected structure
          const formattedHistory = history.map(msg => ({
            sender: msg.role === 'user' ? 'You' : 'Kairos',
            text: msg.content
          }));
          setChatMessages(formattedHistory);
        } else {
           setChatMessages([{ sender: "Kairos", text: "Could not load your previous chat history." }]);
        }
      } catch (error) {
        console.error("Failed to fetch chat history:", error);
        setChatMessages([{ sender: "Kairos", text: "Error connecting to the server." }]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, [userId]);

  // --- 3. Connect to WebSocket ---
  useEffect(() => {
    if (!userId) return; // Don't connect until we have a user ID

    console.log(`Attempting to connect WebSocket for user: ${userId}`);
    const ws = new WebSocket(`${WS_URL}/api/chat/ws/${userId}`);

    ws.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
       // Assuming the backend sends back a message in the format { role: 'bot', content: '...' }
      const formattedMessage = {
        sender: message.role === 'user' ? 'You' : 'Kairos',
        text: message.content
      };
      setChatMessages((prevMessages) => [...prevMessages, formattedMessage]);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    websocket.current = ws;

    // Cleanup on component unmount
    return () => {
      ws.close();
    };
  }, [userId]);

  // --- 4. Auto-scroll to the latest message ---
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // --- 5. Send a message ---
  const handleSend = () => {
    if (chatInput.trim() === "" || !websocket.current || websocket.current.readyState !== WebSocket.OPEN) {
        return;
    }

    const messageToSend = {
      message: chatInput, // This matches what the backend's Pydantic model expects
    };

    websocket.current.send(JSON.stringify(messageToSend));
    
    // Optimistically add the user's message to the UI
    const userMessage = { sender: "You", text: chatInput };
    setChatMessages((prev) => [...prev, userMessage]);
    setChatInput("");
  };
  
  // (Your ChatMessage and other JSX components remain the same)
  // ... Paste your existing ChatMessage component and the main return JSX here ...
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
    <div className="bg-[#a7ebf2] min-h-[84.5vh] flex flex-col p-4 relative overflow-hidden">
      <main className="flex-1 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1 flex flex-col bg-[#023859] rounded-lg shadow-xl overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b-2 border-gray-700 flex-shrink-0">
              <div className="flex items-center">
                <div className="rounded-full mr-4 w-10 h-10">
                  <Image src="/chatbot_logo.svg" alt="Kairos" width={40} height={40}/>
                </div>
                <div>
                  <p className="font-semibold text-[#a7ebf2]">Kairos</p>
                  <p className="text-xs text-gray-400">Your wellness companion</p>
                </div>
              </div>
          </div>
          <div className="flex-1 p-4 overflow-y-auto" style={{ height: "calc(100vh - 240px)" }}>
            <div className="max-w-4xl mx-auto space-y-4">
              {isLoading ? (
                <p className="text-center text-gray-400">Loading history...</p>
              ) : (
                chatMessages.map((msg, idx) => <ChatMessage key={idx} msg={msg} />)
              )}
              <div ref={messageEndRef} />
            </div>
          </div>
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
                className="p-3 rounded-full hover:bg-[#01295c] transition-colors flex items-center justify-center flex-shrink-0 bg-[#011c40] cursor-pointer"
                onClick={handleSend}
              >
                <Image src="/send.svg" alt="Send" width={20} height={20} />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
