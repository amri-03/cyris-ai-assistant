import {useEffect, useState, useRef} from "react";
import api from "../services/api";
import Header from "../components/Header";
import ConversationThread from "../components/ConversationThread";
import MessageInput from "../components/MessageInput";
import SettingsPanel from "../components/SettingsPanel";
import Sidebar from "../components/Sidebar";

const starterCards = [
    {
        title: "Refine an idea",
        subtitle: "Brainstorm design concepts for a new dashboard or app layout.",
        prompt: "Let's brainstorm a premium design concept for an adaptive dashboard.",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
            </svg>
        )
    },
    {
        title: "Analyze codebase",
        subtitle: "Review design patterns, styling strategies, and structures.",
        prompt: "Help me review the architectural patterns and state management in this project.",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="4 17 10 11 4 5"></polyline>
                <line x1="12" y1="19" x2="20" y2="19"></line>
            </svg>
        )
    },
    {
        title: "Draft UI copy",
        subtitle: "Write clear, active, and understated user interface messages.",
        prompt: "Write a compelling, understated landing page headline for a developer tool.",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
        )
    }
];

export default function Home() {
    const [messages, setMessages] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [activeSessionId, setActiveSessionId] = useState(null);
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    
    const [isThinking, setIsThinking] = useState(false);
    const [isConnected, setIsConnected] = useState(true);
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    
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
            setSessions(res.data.sessions || []);
        } catch (error) {
            console.error("Failed to fetch sessions", error);
        }
    };

    const loadSessionMessages = async (sessionId) => {
        try {
            const res = await api.get(`/sessions/${sessionId}/messages`);
            setMessages(res.data.messages || []);
        } catch (error) {
            console.error("Failed to load session messages", error);
        }
    };

    useEffect(() => {
        scrollToBottom("smooth", true);
    }, [messages, isThinking]);

    useEffect(() => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;
        

        fetchSessions().then(() => {
            // We do NOT auto-start a session anymore.
            // Just leave activeSessionId as null (Empty State)
        });
    }, []);

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

    const handleSend = async (text) => {
        // Optimistically add user message
        const userMessage = {role: "user", content: text};
        setMessages((prev) => [...prev, userMessage]);
        setIsThinking(true);

        try {
            const payload = { prompt: text };
            if (activeSessionId) {
                payload.session_id = activeSessionId;
            }

            const response = await api.post("/chat", payload);
            
            const content = response.data.response || "No response available.";
            const returnedSessionId = response.data.session_id;

            setMessages((prev) => [
                ...prev,
                {role: "assistant", content, animate: true},
            ]);

            if (returnedSessionId && returnedSessionId !== activeSessionId) {
                setActiveSessionId(returnedSessionId);
                // Refresh sessions to show the new one in the sidebar
                fetchSessions();
            }

            setIsConnected(true);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: "I wasn't able to reach the backend. Please check that the server is running.",
                },
            ]);
            setIsConnected(false);
        } finally {
            setIsThinking(false);
        }
    };

    const handleSelectSession = (sessionId) => {
        if (activeSessionId === sessionId) return;
        setActiveSessionId(sessionId);
        setMessages([]); // clear current view
        loadSessionMessages(sessionId);
        
        // On mobile, we might want to auto-close the sidebar here
        if (window.innerWidth < 768) {
            setIsSidebarOpen(false);
        }
    };

    const handleNewChat = () => {
        setActiveSessionId(null);
        setMessages([]);
        if (window.innerWidth < 768) {
            setIsSidebarOpen(false);
        }
    };

    const handleDeleteSession = async (sessionId) => {
        try {
            await api.delete(`/sessions/${sessionId}`);
            setSessions(prev => prev.filter(s => s.id !== sessionId));
            if (activeSessionId === sessionId) {
                handleNewChat();
            }
        } catch (error) {
            console.error("Failed to delete session", error);
        }
    };

    return (
        <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', background: 'var(--bg-base)' }}>
            
            {/* SIDEBAR */}
            <Sidebar 
                isOpen={isSidebarOpen}
                sessions={sessions}
                activeSessionId={activeSessionId}
                onSelectSession={handleSelectSession}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
            />

            {/* MAIN CONTENT AREA */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
                
                {/* FIXED HEADER */}
                <div className="glass-header">
                    <div style={{
                        width: "100%",
                        maxWidth: "1400px",
                        margin: "0 auto",
                        padding: "0 24px",
                        display: 'flex',
                        alignItems: 'center'
                    }}>
                        {!isSidebarOpen && (
                            <button
                                onClick={() => setIsSidebarOpen(true)}
                                style={{
                                    background: 'transparent',
                                    border: 'none',
                                    color: 'var(--text-secondary)',
                                    cursor: 'pointer',
                                    padding: '8px',
                                    marginRight: '16px',
                                    borderRadius: 'var(--radius-sm)'
                                }}
                                title="Open Sidebar"
                            >
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                    <line x1="9" y1="3" x2="9" y2="21"></line>
                                </svg>
                            </button>
                        )}
                        <div style={{ flex: 1 }}>
                            <Header 
                                isConnected={isConnected}
                                onOpenSettings={() => setIsSettingsOpen(true)}
                                onConcludeSession={handleNewChat} // Conclude session is basically New Chat now
                                activeSessionTitle={sessions.find(s => s.id === activeSessionId)?.title}
                            />
                        </div>
                    </div>
                </div>

                {/* DYNAMIC CONTENT AREA */}
                {messages.length === 0 ? (
                    /* EMPTY STATE */
                    <div style={{
                        flex: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '24px',
                        paddingTop: '92px' // offset for header
                    }}>
                        <div style={{
                            textAlign: 'center',
                            animation: 'messageFadeIn 0.5s ease-out'
                        }}>
                            <div style={{
                                width: '64px',
                                height: '64px',
                                borderRadius: '50%',
                                background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-glow))',
                                margin: '0 auto 20px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                boxShadow: '0 0 20px var(--accent-glow)'
                            }}>
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
                                    <path d="M12 12 2.1 7.1"></path>
                                    <path d="m12 12 7.1-7.1"></path>
                                </svg>
                            </div>
                            <h1 style={{
                                fontSize: '28px',
                                fontWeight: 600,
                                color: 'var(--text-primary)',
                                marginBottom: '8px'
                            }}>
                                Good {new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 18 ? 'afternoon' : 'evening'}
                            </h1>
                            <p style={{
                                color: 'var(--text-secondary)',
                                fontSize: '15px',
                                maxWidth: '400px',
                                margin: '0 auto 32px',
                                fontWeight: 300
                            }}>
                                How can I help you today?
                            </p>
                        </div>
                        
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                            gap: '16px',
                            width: '100%',
                            maxWidth: '820px',
                            margin: '0 auto 28px',
                            animation: 'messageFadeIn 0.6s ease-out'
                        }}>
                            {starterCards.map((card, idx) => (
                                <div
                                    key={idx}
                                    onClick={() => handleSend(card.prompt)}
                                    style={{
                                        background: 'var(--bg-input)',
                                        border: '1px solid var(--border-subtle)',
                                        borderRadius: 'var(--radius-md)',
                                        padding: '18px',
                                        cursor: 'pointer',
                                        transition: 'all var(--transition)',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '6px',
                                        textAlign: 'left'
                                    }}
                                    onMouseEnter={(e) => {
                                        e.currentTarget.style.borderColor = 'var(--accent-dim)';
                                        e.currentTarget.style.background = 'var(--bg-elevated)';
                                        e.currentTarget.style.transform = 'translateY(-2px)';
                                        e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)';
                                    }}
                                    onMouseLeave={(e) => {
                                        e.currentTarget.style.borderColor = 'var(--border-subtle)';
                                        e.currentTarget.style.background = 'var(--bg-input)';
                                        e.currentTarget.style.transform = 'translateY(0)';
                                        e.currentTarget.style.boxShadow = 'none';
                                    }}
                                >
                                    <div style={{
                                        fontSize: '14.5px',
                                        fontWeight: 600,
                                        color: 'var(--text-primary)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px'
                                    }}>
                                        {card.icon}
                                        {card.title}
                                    </div>
                                    <div style={{
                                        fontSize: '12.5px',
                                        color: 'var(--text-secondary)',
                                        lineHeight: '1.4',
                                        fontWeight: 300
                                    }}>
                                        {card.subtitle}
                                    </div>
                                </div>
                            ))}
                        </div>
                        
                        <div style={{ width: '100%', maxWidth: '820px' }}>
                            <MessageInput onSend={handleSend} isDisabled={isThinking} />
                        </div>
                    </div>
                ) : (
                    /* SCROLLABLE THREAD */
                    <div
                        ref={scrollContainerRef}
                        style={{
                            flex: 1,
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
                                justifyContent: "flex-start",
                            }}
                        >
                            <ConversationThread
                                messages={messages}
                                isThinking={isThinking}
                                onScrollToBottom={scrollToBottom}
                            />
                        </div>
                    </div>
                )}

                {/* FIXED INPUT (ONLY SHOW IF IN A THREAD) */}
                {messages.length > 0 && (
                    <div
                        style={{
                            position: "absolute",
                            bottom: 0,
                            left: 0,
                            width: "100%",
                            zIndex: 10,
                            background: "linear-gradient(to top, var(--bg-base) 70%, transparent)",
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
                )}
            </div>

            {/* SETTINGS DRAWER */}
            <SettingsPanel
                isOpen={isSettingsOpen}
                onClose={() => setIsSettingsOpen(false)}
                currentTheme={theme}
                onThemeChange={(newTheme) => setTheme(newTheme)}
            />
        </div>
    );
}