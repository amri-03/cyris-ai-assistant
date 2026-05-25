export default function ThinkingIndicator() {
    const dotStyle = (delay) => ( {
        width: "5px",
        height: "5px",
        borderRadius: "50%",
        background: "var(--accent-dim)",
        display: "inline-block",
        animation: `dotBounce 1.2s ease-in-out ${delay}s infinite`,
    } );

    return (
        <div
            style={{
                display: "flex",
                alignItems: "flex-start",
                flexDirection: "column",
                gap: "6px",
            }}
        >
            <span
                style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    fontWeight: 500,
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    color: "var(--text-muted)",
                }}
            >
                Cyris
            </span>
            <div
                style={{
                    padding: "14px 20px",
                    borderRadius:
                        "var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm)",
                    background: "var(--cyris-bubble)",
                    border: "1px solid var(--cyris-border)",
                    display: "flex",
                    gap: "6px",
                    alignItems: "center",
                }}
            >
                <span style={dotStyle ( 0 )}/>
                <span style={dotStyle ( 0.2 )}/>
                <span style={dotStyle ( 0.4 )}/>
            </div>
        </div>
    );
}