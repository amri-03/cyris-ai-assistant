import {useEffect, useRef} from "react";
import MessageBubble from "./MessageBubble";
import ThinkingIndicator from "./ThinkingIndicator";

export default function ConversationThread({messages, isThinking}) {
    const bottomRef = useRef ( null );

    useEffect ( () => {
        bottomRef.current?.scrollIntoView ( {behavior: "smooth"} );
    }, [messages, isThinking] );

    const isEmpty = messages.length === 0 && !isThinking;

    return (
        <div
            style={{
                flex: 1,
                padding: "32px 0 24px",
                display: "flex",
                flexDirection: "column",
                gap: "24px",
                position: "relative",
                zIndex: 1,
            }}
        >
            {isEmpty && (
                <div
                    style={{
                        flex: 1,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: "12px",
                        color: "var(--text-muted)",
                        textAlign: "center",
                        paddingTop: "20vh",
                        animation:
                            "messageFadeIn 0.6s cubic-bezier(0.4,0,0.2,1) forwards",
                    }}
                >
                    <span
                        style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            letterSpacing: "0.15em",
                            textTransform: "uppercase",
                            color: "var(--text-muted)",
                        }}
                    >
                        session active
                    </span>
                    <p
                        style={{
                            fontSize: "14px",
                            fontWeight: 300,
                            color: "var(--text-secondary)",
                            maxWidth: "320px",
                            lineHeight: 1.7,
                        }}
                    >
                        Start a conversation. Cyris will
                        remember what matters.
                    </p>
                </div>
            )}

            {messages.map ( (msg, index) => (
                <MessageBubble
                    key={index}
                    role={msg.role}
                    content={msg.content}
                />
            ) )}

            {isThinking && <ThinkingIndicator/>}

            <div ref={bottomRef}/>
        </div>
    );
}