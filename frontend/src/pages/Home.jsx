import {useEffect, useState, useRef} from "react";
import api from "../services/api";
import Header from "../components/Header";
import ConversationThread from "../components/ConversationThread";
import MessageInput from "../components/MessageInput";
import MemoryPanel from "../components/MemoryPanel";
import SettingsPanel from "../components/SettingsPanel";

export default function Home() {
    const [messages, setMessages] = useState ( [] );
    const [isThinking, setIsThinking] = useState ( false );
    const [isConnected, setIsConnected] = useState ( true );
    const [isMemoryOpen, setIsMemoryOpen] = useState(false);
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isReflectionOpen, setIsReflectionOpen] = useState(false);
    const [reflectionSummary, setReflectionSummary] = useState(null);
    const [memoryItems, setMemoryItems] = useState([]);
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

    const fetchMemoryItems = async () => {
        try {
            const response = await api.get("/memory-status");
            setMemoryItems(response.data.continuity_items || []);
        } catch (error) {
            console.error("Failed to fetch memory items", error);
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

    useEffect ( () => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;

        const loadSession = async () => {
            try {
                const historyRes = await api.get("/session-messages");
                const historyMessages = historyRes.data.messages || [];

                // Guard: If user has already sent messages, abort to prevent overwrite
                let alreadyHasMessages = false;
                setMessages(prev => {
                    if (prev.length > 0) {
                        alreadyHasMessages = true;
                    }
                    return prev;
                });
                if (alreadyHasMessages) return;

                if (historyMessages.length > 0) {
                    setMessages(prev => {
                        if (prev.length > 0) return prev;
                        return historyMessages.map(msg => ({
                            role: msg.role,
                            content: msg.content,
                            animate: false,
                            feedback: msg.feedback
                        }));
                    });
                } else {
                    const response = await api.get("/session-start");
                    const message = response.data.message;
                    setMessages(prev => {
                        if (prev.length > 0) return prev;
                        return [
                            {
                                role: "assistant",
                                content: message,
                                animate: false
                            }
                        ];
                    });
                }
            } catch (error) {
                console.error("Session start/reload failed", error);
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
                {role: "assistant", content, animate: true},
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

    const handleConcludeSession = async () => {
        setIsThinking(true);
        try {
            const response = await api.post("/session/conclude");
            if (response.data.status === "success") {
                setReflectionSummary(response.data.summary);
                setIsReflectionOpen(true);
                setMessages([]);
            }
        } catch (error) {
            console.error("Failed to conclude session", error);
        } finally {
            setIsThinking(false);
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
                    zIndex: 10,
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
                        onOpenSettings={() => setIsSettingsOpen(true)}
                        onConcludeSession={handleConcludeSession}
                    />
                </div>
            </div>

            {/* SCROLLABLE THREAD */}
            <div
                ref={scrollContainerRef}
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
                        maxWidth: "820px",
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
                        onScrollToBottom={scrollToBottom}
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
                    zIndex: 10,
                    background:
                        "linear-gradient(to top, var(--bg-base) 70%, transparent)",
                    paddingTop: "24px",
                }}
            >
                <div
                    style={{
                        width: "100%",
                        maxWidth: "820px",
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

            {/* SETTINGS DRAWER */}
            <SettingsPanel
                isOpen={isSettingsOpen}
                onClose={() => setIsSettingsOpen(false)}
                currentTheme={theme}
                onThemeChange={(newTheme) => setTheme(newTheme)}
            />

            {/* REFLECTION OVERLAY MODAL */}
            {isReflectionOpen && (
                <div
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        background: "rgba(0, 0, 0, 0.6)",
                        backdropFilter: "blur(10px)",
                        zIndex: 100,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                    }}
                >
                    <div
                        style={{
                            background: "var(--bg-drawer)",
                            border: "1px solid var(--border-subtle)",
                            borderRadius: "var(--radius-lg)",
                            padding: "40px",
                            maxWidth: "600px",
                            width: "95%",
                            boxShadow: "var(--shadow-modal)",
                            textAlign: "center",
                            animation: "messageFadeIn 0.3s ease-out",
                        }}
                    >
                        <h2
                            style={{
                                fontSize: "22px",
                                fontWeight: 500,
                                marginBottom: "20px",
                                color: "var(--text-accent)",
                                fontFamily: "var(--font-mono)",
                                letterSpacing: "0.05em",
                            }}
                        >
                            SESSION CONCLUDED
                        </h2>
                        <div
                            style={{
                                color: "var(--text-secondary)",
                                fontSize: "14px",
                                lineHeight: "1.7",
                                textAlign: "left",
                                marginBottom: "30px",
                                background: "var(--bg-base)",
                                padding: "20px 24px",
                                borderRadius: "var(--radius-md)",
                                border: "1px solid var(--border-dim)",
                            }}
                        >
                            <p style={{ fontWeight: 500, marginBottom: "12px", color: "var(--text-primary)" }}>
                                Achievements & Commitments:
                            </p>
                            <div style={{ whiteSpace: "pre-line" }}>
                                {reflectionSummary}
                            </div>
                        </div>
                        <button
                            onClick={async () => {
                                setIsReflectionOpen(false);
                                setReflectionSummary(null);
                                try {
                                    setIsThinking(true);
                                    const response = await api.get("/session-start");
                                    const message = response.data.message;
                                    setMessages([
                                        {
                                            role: "assistant",
                                            content: message,
                                        }
                                    ]);
                                    fetchMemoryItems();
                                } catch (err) {
                                    console.error("Failed to load new session", err);
                                } finally {
                                    setIsThinking(false);
                                }
                            }}
                            style={{
                                background: "var(--accent-primary)",
                                color: "#ffffff",
                                border: "none",
                                borderRadius: "var(--radius-sm)",
                                padding: "12px 28px",
                                fontSize: "14px",
                                fontWeight: 500,
                                cursor: "pointer",
                                transition: "opacity var(--transition)",
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.opacity = 0.9}
                            onMouseLeave={(e) => e.currentTarget.style.opacity = 1}
                        >
                            Start New Session
                        </button>
                    </div>
                </div>
            )}

        </div>
    );
}