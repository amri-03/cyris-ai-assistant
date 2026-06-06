import {useEffect, useRef, useState} from "react";
import api from "../services/api";

function CodeBlock({ language, code }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div 
            style={{
                background: "var(--bg-code-block)",
                border: "1px solid var(--border-code)",
                borderRadius: "8px",
                overflow: "hidden",
                margin: "12px 0 16px",
                display: "flex",
                flexDirection: "column",
                maxWidth: "100%",
                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)"
            }}
        >
            {/* Header bar */}
            <div 
                style={{
                    background: "var(--bg-code-header)",
                    padding: "8px 16px",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1px solid var(--border-code)",
                    fontFamily: "var(--font-sans)",
                    fontSize: "13px",
                    color: "var(--text-secondary)"
                }}
            >
                <span style={{ fontWeight: 500, textTransform: "lowercase", fontFamily: "var(--font-mono)", fontSize: "12px" }}>{language}</span>
                <button 
                    onClick={handleCopy}
                    style={{
                        background: "transparent",
                        border: "none",
                        color: "var(--text-secondary)",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: "6px",
                        fontSize: "12px",
                        fontFamily: "var(--font-sans)",
                        transition: "color var(--transition)"
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.color = "var(--text-primary)"}
                    onMouseLeave={(e) => e.currentTarget.style.color = "var(--text-secondary)"}
                >
                    {copied ? (
                        <>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            <span>Copied</span>
                        </>
                    ) : (
                        <>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                            <span>Copy code</span>
                        </>
                    )}
                </button>
            </div>
            
            {/* Code content */}
            <pre 
                style={{
                    margin: 0,
                    padding: "16px",
                    overflowX: "auto",
                    fontFamily: "var(--font-mono)",
                    fontSize: "13.5px",
                    lineHeight: "1.55",
                    color: "var(--text-code)",
                    whiteSpace: "pre",
                    wordBreak: "normal"
                }}
            >
                <code>{code}</code>
            </pre>
        </div>
    );
}

const renderInlineSpans = (text) => {
    if (!text) return "";

    const codeParts = text.split("`");
    return codeParts.map((codePart, codeIndex) => {
        const isInlineCode = codeIndex % 2 === 1;
        if (isInlineCode) {
            return (
                <code 
                    key={`code-${codeIndex}`}
                    style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "13.5px",
                        background: "var(--bg-elevated)",
                        border: "1px solid var(--border-subtle)",
                        borderRadius: "4px",
                        padding: "2px 6px",
                        color: "var(--text-accent)",
                        wordBreak: "break-word"
                    }}
                >
                    {codePart}
                </code>
            );
        } else {
            const boldParts = codePart.split("**");
            return boldParts.map((boldPart, boldIndex) => {
                const isBold = boldIndex % 2 === 1;
                if (isBold) {
                    return (
                        <strong key={`bold-${boldIndex}`} style={{ fontWeight: 600, color: "var(--text-primary)" }}>
                            {boldPart}
                        </strong>
                    );
                } else {
                    return boldPart;
                }
            });
        }
    });
};

const renderParagraphs = (text, partIndex) => {
    const lines = text.split("\n");
    let elements = [];
    let currentList = null;
    let listType = null;

    const pushCurrentList = () => {
        if (currentList) {
            const Tag = listType === "ol" ? "ol" : "ul";
            elements.push(
                <Tag 
                    key={`list-${elements.length}`} 
                    style={{ 
                        margin: "12px 0 16px", 
                        paddingLeft: "24px",
                        display: "flex",
                        flexDirection: "column",
                        gap: "8px"
                    }}
                >
                    {currentList}
                </Tag>
            );
            currentList = null;
            listType = null;
        }
    };

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // Headers (e.g. "### Title" or "## Title")
        const headingMatch = line.match(/^(#{1,6})\s+(.*)$/);
        if (headingMatch) {
            pushCurrentList();
            const level = headingMatch[1].length;
            const content = headingMatch[2];
            const Tag = `h${level}`;
            const headingStyle = {
                fontFamily: "var(--font-sans)",
                fontWeight: 600,
                color: "var(--text-primary)",
                marginTop: level === 1 ? "24px" : "18px",
                marginBottom: "10px",
                lineHeight: "1.4",
            };
            if (level === 1) headingStyle.fontSize = "22px";
            else if (level === 2) headingStyle.fontSize = "18px";
            else headingStyle.fontSize = "16.5px";

            elements.push(
                <Tag key={`h-${i}`} style={headingStyle}>
                    {renderInlineSpans(content)}
                </Tag>
            );
            continue;
        }

        // Ordered list (e.g. "1. Item")
        const olMatch = line.match(/^(\d+)\.\s+(.*)$/);
        if (olMatch) {
            if (listType !== "ol") {
                pushCurrentList();
                listType = "ol";
                currentList = [];
            }
            const content = olMatch[2];
            currentList.push(
                <li 
                    key={`li-${i}`} 
                    style={{ 
                        fontFamily: "var(--font-sans)",
                        fontSize: "16px", 
                        lineHeight: "1.7", 
                        color: "var(--text-primary)" 
                    }}
                >
                    {renderInlineSpans(content)}
                </li>
            );
            continue;
        }

        // Unordered list (e.g. "* Item" or "- Item")
        const ulMatch = line.match(/^([*\-])\s+(.*)$/);
        if (ulMatch) {
            if (listType !== "ul") {
                pushCurrentList();
                listType = "ul";
                currentList = [];
            }
            const content = ulMatch[2];
            currentList.push(
                <li 
                    key={`li-${i}`} 
                    style={{ 
                        fontFamily: "var(--font-sans)",
                        fontSize: "16px", 
                        lineHeight: "1.7", 
                        color: "var(--text-primary)" 
                    }}
                >
                    {renderInlineSpans(content)}
                </li>
            );
            continue;
        }

        // Blank lines
        if (line.trim() === "") {
            pushCurrentList();
            elements.push(<div key={`space-${i}`} style={{ height: "8px" }} />);
            continue;
        }

        // Regular paragraph line
        pushCurrentList();
        elements.push(
            <p 
                key={`p-${i}`} 
                style={{ 
                    fontFamily: "var(--font-sans)",
                    fontSize: "16px", 
                    lineHeight: "1.7", 
                    color: "var(--text-primary)",
                    marginBottom: "12px" 
                }}
            >
                {renderInlineSpans(line)}
            </p>
        );
    }

    pushCurrentList();
    return <div key={`part-${partIndex}`}>{elements}</div>;
};

const renderFormattedText = (text) => {
    if (!text) return null;

    const parts = text.split("```");
    return parts.map((part, index) => {
        const isCodeBlock = index % 2 === 1;
        if (isCodeBlock) {
            const lines = part.split("\n");
            const firstLine = lines[0].trim();
            const language = firstLine || "code";
            const code = lines.slice(1).join("\n").replace(/\n$/, "");

            return (
                <CodeBlock key={index} language={language} code={code} />
            );
        } else {
            return renderParagraphs(part, index);
        }
    });
};

export default function MessageBubble({ role, content, isLatest, onScrollToBottom }) {
    const ref = useRef(null);
    const isUser = role === "user";
    const [displayedContent, setDisplayedContent] = useState(isUser ? content : "");
    const [isTypingComplete, setIsTypingComplete] = useState(isUser);
    const [copied, setCopied] = useState(false);
    const [feedback, setFeedback] = useState(null);

    const isLatestRef = useRef(isLatest);
    const onScrollToBottomRef = useRef(onScrollToBottom);

    useEffect(() => {
        isLatestRef.current = isLatest;
        onScrollToBottomRef.current = onScrollToBottom;
    }, [isLatest, onScrollToBottom]);

    useEffect(() => {
        if (ref.current) {
            ref.current.style.animation = "none";
            void ref.current.offsetHeight;
            ref.current.style.animation = "messageFadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards";
        }
    }, []);

    useEffect(() => {
        if (role === "user") {
            setIsTypingComplete(true);
            setDisplayedContent(content);
            return;
        }

        const safeContent = typeof content === "string" ? content : JSON.stringify(content);
        const words = safeContent.split(" ");
        let index = 0;
        setDisplayedContent("");
        setIsTypingComplete(false);

        const interval = setInterval(() => {
            setDisplayedContent(words.slice(0, index + 1).join(" "));
            index++;

            if (isLatestRef.current && onScrollToBottomRef.current) {
                onScrollToBottomRef.current("auto");
            }

            if (index >= words.length) {
                clearInterval(interval);
                setIsTypingComplete(true);
                if (isLatestRef.current && onScrollToBottomRef.current) {
                    setTimeout(() => {
                        onScrollToBottomRef.current?.("smooth");
                    }, 50);
                }
            }
        }, 25);

        return () => clearInterval(interval);
    }, [content, role]);

    const handleCopy = () => {
        const safeContent = typeof content === "string" ? content : JSON.stringify(content);
        navigator.clipboard.writeText(safeContent);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const safeContent = typeof content === "string" ? content : JSON.stringify(content);

    const handleFeedback = async (val) => {
        const newVal = feedback === val ? null : val;
        setFeedback(newVal);
        try {
            await api.post("/message/feedback", {
                content: safeContent,
                feedback: newVal
            });
        } catch (error) {
            console.error("Failed to save message feedback", error);
        }
    };

    return (
        <div
            ref={ref}
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start",
                gap: "6px",
                opacity: 0,
                animation: "messageFadeIn 0.35s cubic-bezier(0.4,0,0.2,1) forwards",
            }}
        >
            <span
                style={{
                    fontFamily: "var(--font-sans)",
                    fontSize: "11.5px",
                    fontWeight: 600,
                    letterSpacing: "0.05em",
                    textTransform: "uppercase",
                    color: isUser ? "var(--text-accent)" : "var(--text-muted)",
                    paddingLeft: isUser ? 0 : "2px",
                    paddingRight: isUser ? "2px" : 0,
                    marginBottom: "2px"
                }}
            >
                {isUser ? "You" : "Cyris"}
            </span>

            {isUser ? (
                <div
                    style={{
                        maxWidth: "80%",
                        padding: "12px 18px",
                        borderRadius: "18px",
                        background: "var(--user-bubble)",
                        border: "1px solid var(--user-border)",
                        color: "var(--text-primary)",
                        fontFamily: "var(--font-sans)",
                        fontSize: "16px",
                        lineHeight: "1.6",
                        fontWeight: 400,
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-word",
                    }}
                >
                    {safeContent}
                </div>
            ) : (
                <div style={{ width: "100%" }}>
                    <div
                        style={{
                            color: "var(--text-primary)",
                            fontFamily: "var(--font-sans)",
                            fontSize: "16px",
                            lineHeight: "1.7",
                            fontWeight: 400,
                            wordBreak: "break-word",
                            paddingLeft: "2px",
                        }}
                    >
                        {renderFormattedText(displayedContent)}
                    </div>

                    {!isUser && isTypingComplete && (
                        <div 
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: "8px",
                                marginTop: "12px",
                                opacity: 0,
                                animation: "messageFadeIn 0.3s ease-out forwards",
                            }}
                        >
                            {/* Thumbs Up Button */}
                            <button
                                onClick={() => handleFeedback("like")}
                                title="Like response"
                                style={{
                                    background: "transparent",
                                    border: "1px solid " + (feedback === "like" ? "var(--accent-primary)" : "var(--border-subtle)"),
                                    color: feedback === "like" ? "var(--accent-primary)" : "var(--text-secondary)",
                                    cursor: "pointer",
                                    padding: "6px",
                                    borderRadius: "var(--radius-sm)",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    width: "28px",
                                    height: "28px",
                                    transition: "all var(--transition)",
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.color = feedback === "like" ? "var(--accent-primary)" : "var(--text-primary)";
                                    e.currentTarget.style.borderColor = feedback === "like" ? "var(--accent-primary)" : "var(--user-border)";
                                    e.currentTarget.style.background = "var(--bg-elevated)";
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.color = feedback === "like" ? "var(--accent-primary)" : "var(--text-secondary)";
                                    e.currentTarget.style.borderColor = feedback === "like" ? "var(--accent-primary)" : "var(--border-subtle)";
                                    e.currentTarget.style.background = "transparent";
                                }}
                            >
                                <svg 
                                    width="14" 
                                    height="14" 
                                    viewBox="0 0 24 24" 
                                    fill={feedback === "like" ? "currentColor" : "none"} 
                                    stroke="currentColor" 
                                    strokeWidth="2" 
                                    strokeLinecap="round" 
                                    strokeLinejoin="round"
                                >
                                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                                </svg>
                            </button>

                            {/* Thumbs Down Button */}
                            <button
                                onClick={() => handleFeedback("dislike")}
                                title="Dislike response"
                                style={{
                                    background: "transparent",
                                    border: "1px solid " + (feedback === "dislike" ? "#ef4444" : "var(--border-subtle)"),
                                    color: feedback === "dislike" ? "#ef4444" : "var(--text-secondary)",
                                    cursor: "pointer",
                                    padding: "6px",
                                    borderRadius: "var(--radius-sm)",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    width: "28px",
                                    height: "28px",
                                    transition: "all var(--transition)",
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.color = feedback === "dislike" ? "#ef4444" : "var(--text-primary)";
                                    e.currentTarget.style.borderColor = feedback === "dislike" ? "#ef4444" : "var(--user-border)";
                                    e.currentTarget.style.background = "var(--bg-elevated)";
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.color = feedback === "dislike" ? "#ef4444" : "var(--text-secondary)";
                                    e.currentTarget.style.borderColor = feedback === "dislike" ? "#ef4444" : "var(--border-subtle)";
                                    e.currentTarget.style.background = "transparent";
                                }}
                            >
                                <svg 
                                    width="14" 
                                    height="14" 
                                    viewBox="0 0 24 24" 
                                    fill={feedback === "dislike" ? "currentColor" : "none"} 
                                    stroke="currentColor" 
                                    strokeWidth="2" 
                                    strokeLinecap="round" 
                                    strokeLinejoin="round"
                                >
                                    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"/>
                                </svg>
                            </button>

                            {/* Copy Button */}
                            <button
                                onClick={handleCopy}
                                title={copied ? "Copied!" : "Copy response"}
                                style={{
                                    background: "transparent",
                                    border: "1px solid var(--border-subtle)",
                                    color: copied ? "var(--accent-primary)" : "var(--text-secondary)",
                                    cursor: "pointer",
                                    padding: "6px",
                                    borderRadius: "var(--radius-sm)",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    width: "28px",
                                    height: "28px",
                                    transition: "all var(--transition)",
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.color = "var(--text-primary)";
                                    e.currentTarget.style.borderColor = "var(--user-border)";
                                    e.currentTarget.style.background = "var(--bg-elevated)";
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.color = copied ? "var(--accent-primary)" : "var(--text-secondary)";
                                    e.currentTarget.style.borderColor = "var(--border-subtle)";
                                    e.currentTarget.style.background = "transparent";
                                }}
                            >
                                {copied ? (
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                        <polyline points="20 6 9 17 4 12"></polyline>
                                    </svg>
                                ) : (
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                    </svg>
                                )}
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}