import {useEffect, useRef} from "react";

export default function MessageBubble({role, content}) {
    const ref = useRef ( null );

    useEffect ( () => {
        if (ref.current) {
            ref.current.style.animation = "none";
            void ref.current.offsetHeight;
            ref.current.style.animation =
                "messageFadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards";
        }
    }, [] );

    const isUser = role === "user";

    return (
        <div
            ref={ref}
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start",
                gap: "6px",
                opacity: 0,
                animation:
                    "messageFadeIn 0.35s cubic-bezier(0.4,0,0.2,1) forwards",
            }}
        >
            {/* Sender label */}
            <span
                style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    fontWeight: 500,
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    color: isUser
                        ? "var(--text-accent)"
                        : "var(--text-muted)",
                    paddingLeft: isUser ? 0 : "2px",
                    paddingRight: isUser ? "2px" : 0,
                }}
            >
                {isUser ? "You" : "Cyris"}
            </span>

            {/* Bubble */}
            <div
                style={{
                    maxWidth: "78%",
                    padding: "14px 18px",
                    borderRadius: isUser
                        ? "var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg)"
                        : "var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm)",
                    background: isUser
                        ? "var(--user-bubble)"
                        : "var(--cyris-bubble)",
                    border: `1px solid ${
                        isUser
                            ? "var(--user-border)"
                            : "var(--cyris-border)"
                    }`,
                    color: "var(--text-primary)",
                    fontFamily: "var(--font-sans)",
                    fontSize: "14.5px",
                    lineHeight: "1.65",
                    fontWeight: 300,
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                    boxShadow: isUser
                        ? "0 0 20px rgba(123, 108, 255, 0.06)"
                        : "none",
                }}
            >
                {content}
            </div>
        </div>
    );
}