export default function Header({isConnected}) {
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
                        fontSize: "18px",
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
                        fontSize: "10px",
                        fontWeight: 300,
                        letterSpacing: "0.15em",
                        textTransform: "uppercase",
                        color: "var(--text-muted)",
                    }}
                >
                    adaptive
                </span>
            </div>

            {/* Connection status */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "7px",
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
                        fontSize: "10px",
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
    );
}