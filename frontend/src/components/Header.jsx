export default function Header({isConnected, onOpenMemory, onOpenSettings, onConcludeSession}) {
    return (
        <div
            style={{
                paddingTop: "28px",
                paddingBottom: "20px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                borderBottom: "1px solid var(--border-dim)",
                position: "relative",
                zIndex: 1,
                flexShrink: 0,
            }}
        >
            {/* Wordmark */}
            <div style={{display: "flex", alignItems: "baseline", gap: "10px"}}>
                <span
                    style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "22px",
                        fontWeight: 500,
                        letterSpacing: "0.12em",
                        textTransform: "uppercase",
                        color: "var(--text-primary)",
                    }}
                >
                    Cyris
                </span>
                <span
                    style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "12px",
                        fontWeight: 300,
                        letterSpacing: "0.15em",
                        textTransform: "uppercase",
                        color: "var(--text-muted)",
                    }}
                >
                    adaptive
                </span>
            </div>

            {/* Action buttons & Connection status */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "16px",
                }}
            >
                {/* Conclude Session button */}
                <button
                    onClick={onConcludeSession}
                    title="Conclude Session"
                    style={{
                        background: "transparent",
                        border: "1px solid var(--border-subtle)",
                        borderRadius: "var(--radius-sm)",
                        padding: "8px 10px",
                        color: "var(--text-secondary)",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        lineHeight: 1,
                        transition: "all var(--transition)",
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "#4ade80";
                        e.currentTarget.style.color = "#4ade80";
                        e.currentTarget.style.background = "var(--bg-elevated)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "var(--border-subtle)";
                        e.currentTarget.style.color = "var(--text-secondary)";
                        e.currentTarget.style.background = "transparent";
                    }}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                </button>

                {/* Memory panel button */}
                <button
                    onClick={onOpenMemory}
                    title="Memory Profile"
                    style={{
                        background: "transparent",
                        border: "1px solid var(--border-subtle)",
                        borderRadius: "var(--radius-sm)",
                        padding: "8px 10px",
                        color: "var(--text-secondary)",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        lineHeight: 1,
                        transition: "all var(--transition)",
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "var(--user-border)";
                        e.currentTarget.style.color = "var(--text-primary)";
                        e.currentTarget.style.background = "var(--bg-elevated)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "var(--border-subtle)";
                        e.currentTarget.style.color = "var(--text-secondary)";
                        e.currentTarget.style.background = "transparent";
                    }}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>
                        <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>
                        <path d="M12 5v14"/>
                        <path d="M12 9h4"/>
                        <path d="M12 14h-4"/>
                    </svg>
                </button>

                {/* Settings button */}
                <button
                    onClick={onOpenSettings}
                    title="Settings"
                    style={{
                        background: "transparent",
                        border: "1px solid var(--border-subtle)",
                        borderRadius: "var(--radius-sm)",
                        padding: "8px 10px",
                        color: "var(--text-secondary)",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        lineHeight: 1,
                        transition: "all var(--transition)",
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "var(--user-border)";
                        e.currentTarget.style.color = "var(--text-primary)";
                        e.currentTarget.style.background = "var(--bg-elevated)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "var(--border-subtle)";
                        e.currentTarget.style.color = "var(--text-secondary)";
                        e.currentTarget.style.background = "transparent";
                    }}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.1a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                        <circle cx="12" cy="12" r="3"/>
                    </svg>
                </button>

                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "7px",
                        marginLeft: "8px"
                    }}
                >
                    <span
                        style={{
                            width: "6px",
                            height: "6px",
                            borderRadius: "50%",
                            background: isConnected
                                ? "#4ade80"
                                : "var(--text-muted)",
                            boxShadow: isConnected
                                ? "0 0 8px rgba(74, 222, 128, 0.6)"
                                : "none",
                            transition: "all var(--transition)",
                        }}
                    />
                    <span
                        style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            letterSpacing: "0.12em",
                            textTransform: "uppercase",
                            color: isConnected
                                ? "var(--text-secondary)"
                                : "var(--text-muted)",
                        }}
                    >
                        {isConnected ? "online" : "offline"}
                    </span>
                </div>
            </div>
        </div>
    );
}