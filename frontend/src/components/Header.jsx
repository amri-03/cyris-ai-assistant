export default function Header({isConnected, onOpenSettings, onConcludeSession, activeSessionTitle}) {
    return (
        <div
            style={{
                paddingTop: "18px",
                paddingBottom: "18px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                position: "relative",
                zIndex: 1,
                flexShrink: 0,
            }}
        >
            {/* Left side spacer / placeholder */}
            <div style={{ minWidth: "1px", height: "1px" }} />

            {/* Center: Session Title */}
            <div style={{
                position: "absolute",
                left: "50%",
                transform: "translateX(-50%)",
                display: "flex",
                alignItems: "center",
                pointerEvents: "none"
            }}>
                <span
                    style={{
                        fontFamily: "var(--font-sans)",
                        fontSize: "14px",
                        fontWeight: 500,
                        color: "var(--text-secondary)",
                        whiteSpace: "nowrap",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        maxWidth: "400px"
                    }}
                >
                    {activeSessionTitle || ""}
                </span>
            </div>

            {/* Action buttons & Connection status */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                }}
            >
                {/* Conclude Session button */}
                <button
                    onClick={onConcludeSession}
                    title="Conclude Current Session"
                    style={{
                        background: "transparent",
                        border: "1px solid var(--border-subtle)",
                        borderRadius: "var(--radius-sm)",
                        padding: "8px 14px",
                        color: "var(--text-secondary)",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        fontSize: "13px",
                        fontFamily: "var(--font-mono)",
                        letterSpacing: "0.05em",
                        transition: "all var(--transition)",
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "var(--accent-primary)";
                        e.currentTarget.style.color = "var(--accent-primary)";
                        e.currentTarget.style.background = "var(--accent-glow)";
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "var(--border-subtle)";
                        e.currentTarget.style.color = "var(--text-secondary)";
                        e.currentTarget.style.background = "transparent";
                    }}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                    <span>Conclude</span>
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
                        e.currentTarget.style.borderColor = "var(--accent-primary)";
                        e.currentTarget.style.color = "var(--accent-primary)";
                        e.currentTarget.style.background = "var(--accent-glow)";
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