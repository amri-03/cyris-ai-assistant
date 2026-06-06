import {useEffect, useRef, useState} from "react";

export default function MessageBubble({
                                          role,
                                          content
                                      }) {

    const ref = useRef ( null );

    const isUser = role === "user";
    const [displayedContent, setDisplayedContent] = useState(isUser ? content : "");
    const [isTypingComplete, setIsTypingComplete] = useState(isUser);
    const [copied, setCopied] = useState(false);

    useEffect ( () => {

        if (ref.current) {

            ref.current.style.animation = "none";

            void ref.current.offsetHeight;

            ref.current.style.animation =
                "messageFadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards";
        }

    }, [] );

    useEffect ( () => {

        if (role === "user") {
            setIsTypingComplete(true);
            setDisplayedContent(content);
            return;
        }

        const safeContent =
            typeof content === "string"
                ? content
                : JSON.stringify ( content );

        const words =
            safeContent.split ( " " );

        let index = 0;
        setDisplayedContent("");
        setIsTypingComplete(false);

        const interval = setInterval ( () => {

            setDisplayedContent (
                words
                    .slice ( 0, index + 1 )
                    .join ( " " )
            );

            index++;

            if (index >= words.length) {
                clearInterval ( interval );
                setIsTypingComplete(true);
            }

        }, 45 );

        return () => clearInterval ( interval );

    }, [content, role] );

    const handleCopy = () => {
        const safeContent =
            typeof content === "string"
                ? content
                : JSON.stringify ( content );
        navigator.clipboard.writeText(safeContent);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const safeContent =
        typeof content === "string"
            ? content
            : JSON.stringify ( content );

    return (

        <div
            ref={ref}
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: isUser
                    ? "flex-end"
                    : "flex-start",
                gap: "6px",
                opacity: 0,
                animation:
                    "messageFadeIn 0.35s cubic-bezier(0.4,0,0.2,1) forwards",
            }}
        >

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
                    paddingLeft: isUser
                        ? 0
                        : "2px",
                    paddingRight: isUser
                        ? "2px"
                        : 0,
                }}
            >
                {isUser ? "You" : "Cyris"}
            </span>

            {
                isUser ? (

                    <div
                        style={{
                            maxWidth: "78%",
                            padding: "14px 18px",
                            borderRadius:
                                "var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg)",
                            background:
                                "var(--user-bubble)",
                            border:
                                "1px solid var(--user-border)",
                            color:
                                "var(--text-primary)",
                            fontFamily:
                                "var(--font-sans)",
                            fontSize: "14.5px",
                            lineHeight: "1.65",
                            fontWeight: 300,
                            whiteSpace: "pre-wrap",
                            wordBreak: "break-word",
                            boxShadow:
                                "0 0 20px rgba(123, 108, 255, 0.06)",
                        }}
                    >
                        {safeContent}
                    </div>

                ) : (

                    <div style={{ maxWidth: "78%" }}>
                        <div
                            style={{
                                color:
                                    "var(--text-primary)",
                                fontFamily:
                                    "var(--font-sans)",
                                fontSize: "14.5px",
                                lineHeight: "1.9",
                                fontWeight: 300,
                                whiteSpace: "pre-wrap",
                                wordBreak: "break-word",
                                paddingLeft: "2px",
                            }}
                        >
                            {displayedContent}
                        </div>

                        {!isUser && isTypingComplete && (
                            <div 
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "12px",
                                    marginTop: "12px",
                                    opacity: 0,
                                    animation: "messageFadeIn 0.3s ease-out forwards",
                                }}
                            >
                                <button
                                    onClick={handleCopy}
                                    style={{
                                        background: "transparent",
                                        border: "1px solid var(--border-subtle)",
                                        color: "var(--text-secondary)",
                                        fontSize: "11px",
                                        cursor: "pointer",
                                        padding: "4px 8px",
                                        borderRadius: "var(--radius-sm)",
                                        display: "flex",
                                        alignItems: "center",
                                        gap: "5px",
                                        transition: "all var(--transition)",
                                        fontFamily: "var(--font-mono)",
                                        textTransform: "uppercase",
                                        letterSpacing: "0.05em",
                                    }}
                                    onMouseEnter={(e) => {
                                        e.currentTarget.style.color = "var(--text-primary)";
                                        e.currentTarget.style.borderColor = "var(--user-border)";
                                        e.currentTarget.style.background = "var(--bg-elevated)";
                                    }}
                                    onMouseLeave={(e) => {
                                        e.currentTarget.style.color = "var(--text-secondary)";
                                        e.currentTarget.style.borderColor = "var(--border-subtle)";
                                        e.currentTarget.style.background = "transparent";
                                    }}
                                >
                                    {copied ? (
                                        <>
                                            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                                                <polyline points="20 6 9 17 4 12"></polyline>
                                            </svg>
                                            <span>Copied</span>
                                        </>
                                    ) : (
                                        <>
                                            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                            </svg>
                                            <span>Copy</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        )}
                    </div>

                )
            }

        </div>
    );
}