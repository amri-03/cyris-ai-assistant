import {useEffect, useRef, useState} from "react";

export default function MessageBubble({
                                          role,
                                          content
                                      }) {

    const ref = useRef ( null );

    const [displayedContent, setDisplayedContent] =
        useState (
            role === "user"
                ? content
                : ""
        );

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
            return;
        }

        const safeContent =
            typeof content === "string"
                ? content
                : JSON.stringify ( content );

        const words =
            safeContent.split ( " " );

        let index = 0;

        const interval = setInterval ( () => {

            setDisplayedContent (
                words
                    .slice ( 0, index + 1 )
                    .join ( " " )
            );

            index++;

            if (index >= words.length) {
                clearInterval ( interval );
            }

        }, 45 );

        return () => clearInterval ( interval );

    }, [content, role] );

    const isUser = role === "user";

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

                    <div
                        style={{
                            maxWidth: "78%",
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

                )
            }

        </div>
    );
}