import { useEffect, useRef, useState } from "react";
import api from "../services/api";

function CodeBlock({ language, code }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="code-block-container">
            <div className="code-block-header">
                <span className="code-block-lang">{language}</span>
                <button onClick={handleCopy} className="code-copy-btn">
                    {copied ? (
                        <>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                <polyline points="20 6 9 17 4 12" />
                            </svg>
                            <span>Copied</span>
                        </>
                    ) : (
                        <>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                            </svg>
                            <span>Copy code</span>
                        </>
                    )}
                </button>
            </div>
            <pre className="code-block-pre">
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
                <code key={`code-${codeIndex}`} className="inline-code">
                    {codePart}
                </code>
            );
        } else {
            const boldParts = codePart.split("**");
            return boldParts.map((boldPart, boldIndex) => {
                const isBold = boldIndex % 2 === 1;
                if (isBold) {
                    return (
                        <strong key={`bold-${boldIndex}`} className="markdown-strong">
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
                <Tag key={`list-${elements.length}`} className="markdown-list">
                    {currentList}
                </Tag>
            );
            currentList = null;
            listType = null;
        }
    };

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        // Heading match
        const headingMatch = line.match(/^(#{1,6})\s+(.*)$/);
        if (headingMatch) {
            pushCurrentList();
            const level = headingMatch[1].length;
            const content = headingMatch[2];
            const className = level === 1 ? "markdown-h1" : level === 2 ? "markdown-h2" : "markdown-h3";

            if (level === 1) {
                elements.push(<h1 key={`h1-${i}`} className={className}>{renderInlineSpans(content)}</h1>);
            } else if (level === 2) {
                elements.push(<h2 key={`h2-${i}`} className={className}>{renderInlineSpans(content)}</h2>);
            } else {
                elements.push(<h3 key={`h3-${i}`} className={className}>{renderInlineSpans(content)}</h3>);
            }
            continue;
        }

        // Ordered list
        const olMatch = line.match(/^(\d+)\.\s+(.*)$/);
        if (olMatch) {
            if (listType !== "ol") {
                pushCurrentList();
                listType = "ol";
                currentList = [];
            }
            const content = olMatch[2];
            currentList.push(
                <li key={`li-${i}`} className="markdown-li">
                    {renderInlineSpans(content)}
                </li>
            );
            continue;
        }

        // Unordered list
        const ulMatch = line.match(/^([*-])\s+(.*)$/);
        if (ulMatch) {
            if (listType !== "ul") {
                pushCurrentList();
                listType = "ul";
                currentList = [];
            }
            const content = ulMatch[2];
            currentList.push(
                <li key={`li-${i}`} className="markdown-li">
                    {renderInlineSpans(content)}
                </li>
            );
            continue;
        }

        // Blank line
        if (line.trim() === "") {
            pushCurrentList();
            elements.push(<div key={`space-${i}`} className="markdown-spacer" />);
            continue;
        }

        // Paragraph
        pushCurrentList();
        elements.push(
            <p key={`p-${i}`} className="markdown-p">
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

            return <CodeBlock key={index} language={language} code={code} />;
        } else {
            return renderParagraphs(part, index);
        }
    });
};

export default function MessageBubble({ role, content, isLatest, onScrollToBottom, animate, feedback: initialFeedback }) {
    const isUser = role === "user";
    const shouldAnimate = !isUser && animate === true;
    const [displayedContent, setDisplayedContent] = useState(shouldAnimate ? "" : content);
    const [isTypingComplete, setIsTypingComplete] = useState(!shouldAnimate);
    const [copied, setCopied] = useState(false);
    const [feedback, setFeedback] = useState(initialFeedback || null);

    const [prevInitialFeedback, setPrevInitialFeedback] = useState(initialFeedback);
    if (initialFeedback !== prevInitialFeedback) {
        setFeedback(initialFeedback || null);
        setPrevInitialFeedback(initialFeedback);
    }

    const [prevContent, setPrevContent] = useState(content);
    if (content !== prevContent) {
        setPrevContent(content);
        setDisplayedContent(shouldAnimate ? "" : content);
        setIsTypingComplete(!shouldAnimate);
    }

    const isLatestRef = useRef(isLatest);
    const onScrollToBottomRef = useRef(onScrollToBottom);

    useEffect(() => {
        isLatestRef.current = isLatest;
        onScrollToBottomRef.current = onScrollToBottom;
    }, [isLatest, onScrollToBottom]);

    useEffect(() => {
        if (!shouldAnimate) return;

        const safeContent = typeof content === "string" ? content : JSON.stringify(content);
        const words = safeContent.split(" ");
        let index = 0;

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
    }, [content, role, shouldAnimate]);

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
        <div className={`msg-wrapper ${isUser ? "msg-wrapper-user" : "msg-wrapper-assistant"}`}>
            <span className={`msg-role-label ${isUser ? "msg-role-label-user" : "msg-role-label-assistant"}`}>
                {isUser ? "You" : "Cyris"}
            </span>

            {isUser ? (
                <div className="user-bubble-box">{safeContent}</div>
            ) : (
                <div className="assistant-text-box">
                    <div>{renderFormattedText(displayedContent)}</div>

                    {isTypingComplete && (
                        <div className="msg-action-bar">
                            <button
                                onClick={() => handleFeedback("like")}
                                title="Like response"
                                className={`msg-action-btn ${feedback === "like" ? "liked" : ""}`}
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill={feedback === "like" ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                                </svg>
                            </button>

                            <button
                                onClick={() => handleFeedback("dislike")}
                                title="Dislike response"
                                className={`msg-action-btn ${feedback === "dislike" ? "disliked" : ""}`}
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill={feedback === "dislike" ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3" />
                                </svg>
                            </button>

                            <button
                                onClick={handleCopy}
                                title={copied ? "Copied!" : "Copy response"}
                                className={`msg-action-btn ${copied ? "copied" : ""}`}
                            >
                                {copied ? (
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                ) : (
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
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