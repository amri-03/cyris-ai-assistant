import {useEffect, useState, useRef} from "react";
import api from "../services/api";
import Header from "../components/Header";
import ConversationThread from "../components/ConversationThread";
import MessageInput from "../components/MessageInput";
import MemoryPanel from "../components/MemoryPanel";

export default function Home() {
    const [messages, setMessages] = useState ( [] );
    const [isThinking, setIsThinking] = useState ( false );
    const [isConnected, setIsConnected] = useState ( true );
    const [isMemoryOpen, setIsMemoryOpen] = useState(false);
    const [memoryItems, setMemoryItems] = useState([]);
    const hasInitialized = useRef(false);

    const fetchMemoryItems = async () => {
        try {
            const response = await api.get("/memory-status");
            setMemoryItems(response.data.continuity_items || []);
        } catch (error) {
            console.error("Failed to fetch memory items", error);
        }
    };

    useEffect ( () => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;

        const loadSession = async () => {

            try {

                const response =
                    await api.get (
                        "/session-start"
                    );

                const message =
                    response.data.message;

                setMessages ( [
                    {
                        role: "assistant",
                        content: message,
                    }
                ] );

            } catch (error) {

                console.error (
                    "Session start failed",
                    error
                );
            }
        };

        loadSession();
        fetchMemoryItems();

    }, [] );

    const handleSend = async (text) => {
        // Optimistically add user message
        const userMessage = {role: "user", content: text};
        setMessages ( (prev) => [...prev, userMessage] );
        setIsThinking ( true );

        try {
            const response = await api.post ( "/chat", {
                prompt: text,
            } );

            const content =
                response.data.response ||
                "No response available.";

            setMessages ( (prev) => [
                ...prev,
                {role: "assistant", content},
            ] );

            setIsConnected ( true );
            
            // Refresh memory items automatically after response is received
            fetchMemoryItems();
        } catch {
            setMessages ( (prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "I wasn't able to reach the backend. Please check that the server is running.",
                },
            ] );
            setIsConnected ( false );
        } finally {
            setIsThinking ( false );
        }
    };

    const handleDeleteMemoryItem = async (identity) => {
        try {
            await api.delete(`/memory/${identity}`);
            setMemoryItems((prev) => prev.filter((item) => item.identity !== identity));
        } catch (error) {
            console.error("Failed to delete memory item", error);
        }
    };

    return (
        <div
            style={{
                height: "100vh",
                background: "var(--bg-base)",
                overflow: "hidden",
                position: "relative",
            }}
        >

            {/* FIXED HEADER */}
            <div
                style={{
                    position: "fixed",
                    top: 0,
                    left: 0,
                    width: "100%",
                    zIndex: 100,
                    background: "var(--bg-base)",
                }}
            >
                <div
                    style={{
                        width: "100%",
                        maxWidth: "1400px",
                        margin: "0 auto",
                        padding: "0 48px",
                    }}
                >
                    <Header 
                        isConnected={isConnected}
                        onOpenMemory={() => setIsMemoryOpen(true)}
                    />
                </div>
            </div>

            {/* SCROLLABLE THREAD */}
            <div
                style={{
                    height: "100%",
                    overflowY: "auto",
                    paddingTop: "92px",
                    paddingBottom: "140px",
                }}
            >
                <div
                    style={{
                        width: "100%",
                        maxWidth: "760px",
                        margin: "0 auto",
                        minHeight: "100%",
                        display: "flex",
                        flexDirection: "column",
                        justifyContent:
                            messages.length === 0
                                ? "center"
                                : "flex-start",
                    }}
                >

                    <ConversationThread
                        messages={messages}
                        isThinking={isThinking}
                    />

                </div>
            </div>

            {/* FIXED INPUT */}
            <div
                style={{
                    position: "fixed",
                    bottom: 0,
                    left: 0,
                    width: "100%",
                    zIndex: 100,
                    background:
                        "linear-gradient(to top, var(--bg-base) 70%, transparent)",
                    paddingTop: "24px",
                }}
            >
                <div
                    style={{
                        width: "100%",
                        maxWidth: "760px",
                        margin: "0 auto",
                    }}
                >
                    <MessageInput
                        onSend={handleSend}
                        isDisabled={isThinking}
                    />
                </div>
            </div>

            {/* INTERACTIVE MEMORY DRAWER */}
            <MemoryPanel
                isOpen={isMemoryOpen}
                onClose={() => setIsMemoryOpen(false)}
                items={memoryItems}
                onDelete={handleDeleteMemoryItem}
                onReconcile={fetchMemoryItems}
            />

        </div>
    );
}