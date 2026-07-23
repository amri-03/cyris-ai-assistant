import { useEffect, useState, useRef } from "react";
import api from "../services/api";
import Header from "../components/Header";
import ConversationThread from "../components/ConversationThread";
import MessageInput from "../components/MessageInput";
import Sidebar from "../components/Sidebar";
import MemoryPanel from "../components/MemoryPanel";
import SettingsPanel from "../components/SettingsPanel";

export default function Home() {
    const [messages, setMessages] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [activeSessionId, setActiveSessionId] = useState(null);

    const [isSessionDrawerOpen, setIsSessionDrawerOpen] = useState(false);
    const [isMemoryModalOpen, setIsMemoryModalOpen] = useState(false);
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    const [isThinking, setIsThinking] = useState(false);
    const [isConnected, setIsConnected] = useState(true);

    const [theme, setTheme] = useState(() => {
        const saved = localStorage.getItem("cyris-theme");
        return saved === "light" ? "light" : "dark";
    });

    const hasInitialized = useRef(false);
    const scrollContainerRef = useRef(null);

    useEffect(() => {
        document.body.className = `${theme}-theme`;
        localStorage.setItem("cyris-theme", theme);
    }, [theme]);

    const fetchSessions = async () => {
        try {
            const res = await api.get("/sessions");
            setSessions(res.data?.sessions || []);
        } catch (error) {
            console.error("Failed to fetch sessions", error);
        }
    };

    const loadSessionMessages = async (sessionId) => {
        try {
            const res = await api.get(`/sessions/${sessionId}/messages`);
            setMessages(res.data?.messages || []);
        } catch (error) {
            console.error("Failed to load session messages", error);
        }
    };

    const scrollToBottom = (behavior = "smooth", force = false) => {
        if (scrollContainerRef.current) {
            const container = scrollContainerRef.current;
            const isNear = container.scrollHeight - container.scrollTop - container.clientHeight < 200;
            if (force || isNear) {
                container.scrollTo({
                    top: container.scrollHeight,
                    behavior
                });
            }
        }
    };

    useEffect(() => {
        scrollToBottom("smooth", true);
    }, [messages, isThinking]);

    useEffect(() => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;
        fetchSessions();
    }, []);

    const handleSend = async (text) => {
        const nowIso = new Date().toISOString();
        const userMessage = { role: "user", content: text, created_at: nowIso };
        setMessages((prev) => [...prev, userMessage]);
        setIsThinking(true);

        try {
            const payload = { prompt: text };
            if (activeSessionId) {
                payload.session_id = activeSessionId;
            }

            const response = await api.post("/chat", payload);
            const content = response.data?.response || "No response available.";
            const returnedSessionId = response.data?.session_id;

            setMessages((prev) => [
                ...prev,
                { role: "assistant", content, animate: true, created_at: new Date().toISOString() }
            ]);

            if (returnedSessionId && returnedSessionId !== activeSessionId) {
                setActiveSessionId(returnedSessionId);
                fetchSessions();
            }

            setIsConnected(true);
        } catch (error) {
            console.error("Chat request failed", error);
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: "I wasn't able to reach the backend server. Please check that the server is running.",
                    created_at: new Date().toISOString()
                }
            ]);
            setIsConnected(false);
        } finally {
            setIsThinking(false);
        }
    };

    const handleSelectSession = (sessionId) => {
        if (activeSessionId === sessionId) return;
        setActiveSessionId(sessionId);
        setMessages([]);
        loadSessionMessages(sessionId);
    };

    const handleNewChat = () => {
        setActiveSessionId(null);
        setMessages([]);
    };

    const handleDeleteSession = async (sessionId) => {
        try {
            await api.delete(`/sessions/${sessionId}`);
            setSessions((prev) => prev.filter((s) => s.id !== sessionId));
            if (activeSessionId === sessionId) {
                handleNewChat();
            }
        } catch (error) {
            console.error("Failed to delete session", error);
        }
    };

    const activeSession = sessions.find((s) => s.id === activeSessionId);

    return (
        <div className="app-viewport">
            {/* 56px Header Navbar */}
            <Header
                isConnected={isConnected}
                activeSessionTitle={activeSession?.title}
                onOpenSessions={() => setIsSessionDrawerOpen(true)}
                onOpenMemory={() => setIsMemoryModalOpen(true)}
                onOpenSettings={() => setIsSettingsOpen(true)}
                onNewChat={handleNewChat}
            />

            {/* Slide-in Session Drawer */}
            <Sidebar
                isOpen={isSessionDrawerOpen}
                sessions={sessions}
                activeSessionId={activeSessionId}
                onSelectSession={handleSelectSession}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                onClose={() => setIsSessionDrawerOpen(false)}
            />

            {/* Main Centered Thread Workspace */}
            <main className="main-content">
                <div ref={scrollContainerRef} className="thread-scroll-container">
                    <ConversationThread
                        messages={messages}
                        isThinking={isThinking}
                        onScrollToBottom={scrollToBottom}
                        onSendStarter={handleSend}
                    />
                </div>

                {/* Grounded Input Footer */}
                <MessageInput onSend={handleSend} isDisabled={isThinking} />
            </main>

            {/* Continuity Memory Panel */}
            <MemoryPanel
                isOpen={isMemoryModalOpen}
                onClose={() => setIsMemoryModalOpen(false)}
            />

            {/* Settings & Theme Panel */}
            <SettingsPanel
                isOpen={isSettingsOpen}
                onClose={() => setIsSettingsOpen(false)}
                currentTheme={theme}
                onThemeChange={setTheme}
            />
        </div>
    );
}