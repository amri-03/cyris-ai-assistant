import { useEffect } from "react";

export default function Sidebar({
    isOpen,
    sessions,
    activeSessionId,
    onSelectSession,
    onNewChat,
    onDeleteSession,
    onClose
}) {
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            if (e.key === "Escape") {
                onClose();
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [isOpen, onClose]);

    const groupSessions = (sessionsList) => {
        const groups = {
            Today: [],
            "Previous 7 Days": [],
            Older: []
        };

        const now = new Date();
        const todayStr = now.toDateString();

        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(now.getDate() - 7);

        (sessionsList || []).forEach((session) => {
            const updated = new Date(session.updated_at || session.created_at || Date.now());
            if (updated.toDateString() === todayStr) {
                groups.Today.push(session);
            } else if (updated > sevenDaysAgo) {
                groups["Previous 7 Days"].push(session);
            } else {
                groups.Older.push(session);
            }
        });

        return groups;
    };

    const groupedSessions = groupSessions(sessions || []);

    return (
        <>
            {/* Backdrop overlay */}
            <div className={`drawer-overlay ${isOpen ? "open" : ""}`} onClick={onClose} />

            {/* Slide-in drawer */}
            <div className={`session-drawer ${isOpen ? "open" : ""}`}>
                <div className="drawer-header">
                    <div className="drawer-brand">
                        <span>Sessions</span>
                    </div>
                    <button onClick={onClose} className="drawer-close-btn" aria-label="Close sessions drawer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18" />
                            <line x1="6" y1="6" x2="18" y2="18" />
                        </svg>
                    </button>
                </div>

                <button
                    onClick={() => {
                        onNewChat();
                        onClose();
                    }}
                    className="drawer-new-chat-btn"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                    <span>New Session</span>
                </button>

                <div className="drawer-session-list">
                    {Object.entries(groupedSessions).map(([groupName, groupItems]) => {
                        if (groupItems.length === 0) return null;
                        return (
                            <div key={groupName}>
                                <div className="session-group-title">{groupName}</div>
                                {groupItems.map((session) => {
                                    const isActive = activeSessionId === session.id;
                                    return (
                                        <div
                                            key={session.id}
                                            onClick={() => {
                                                onSelectSession(session.id);
                                                onClose();
                                            }}
                                            tabIndex={0}
                                            onKeyDown={(e) => {
                                                if (e.key === "Enter" || e.key === " ") {
                                                    e.preventDefault();
                                                    onSelectSession(session.id);
                                                    onClose();
                                                }
                                            }}
                                            className={`session-item ${isActive ? "active" : ""}`}
                                        >
                                            <span className="session-item-title">
                                                {session.title || "New Session"}
                                            </span>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onDeleteSession(session.id);
                                                }}
                                                className="session-delete-btn"
                                                title="Delete session"
                                            >
                                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                    <path d="M3 6h18" />
                                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                                </svg>
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    })}

                    {(!sessions || sessions.length === 0) && (
                        <div className="memory-empty-state">No previous sessions found.</div>
                    )}
                </div>
            </div>
        </>
    );
}
