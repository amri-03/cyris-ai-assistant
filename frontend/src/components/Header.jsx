export default function Header({
    isConnected,
    activeSessionTitle,
    onOpenSessions,
    onOpenMemory,
    onOpenSettings,
    onNewChat
}) {
    return (
        <header className="header-container">
            {/* Left section: Brand & Session trigger */}
            <div className="header-left">
                <button onClick={onNewChat} className="header-brand-btn" title="New Session">
                    <span>CYRIS</span>
                    <span className="header-brand-tag">AI</span>
                </button>

                <button onClick={onOpenSessions} className="header-session-btn" title="Sessions">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                        <line x1="9" y1="3" x2="9" y2="21" />
                    </svg>
                    <span className="header-session-title">
                        {activeSessionTitle || "New Session"}
                    </span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="6 9 12 15 18 9" />
                    </svg>
                </button>
            </div>

            {/* Right section: Memory, Settings & Connection dot */}
            <div className="header-actions">
                {/* Memory modal trigger */}
                <button onClick={onOpenMemory} className="header-icon-btn" title="Continuity Memory">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12 2a9 9 0 0 1 9 9c0 3.6-2.1 6.7-5.2 8.1L12 22l-3.8-2.9C5.1 17.7 3 14.6 3 11a9 9 0 0 1 9-9z" />
                        <path d="M12 7v5l3 3" />
                    </svg>
                </button>

                {/* Settings / Theme trigger */}
                <button onClick={onOpenSettings} className="header-icon-btn" title="Settings">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.1a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
                        <circle cx="12" cy="12" r="3" />
                    </svg>
                </button>

                {/* Connection dot */}
                <div className="header-status-indicator">
                    <span className={`connection-dot ${isConnected ? "online" : "offline"}`} />
                    <span className={`connection-text ${isConnected ? "online" : ""}`}>
                        {isConnected ? "online" : "offline"}
                    </span>
                </div>
            </div>
        </header>
    );
}