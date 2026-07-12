import {useState, useRef} from "react";

export default function MessageInput({onSend, isDisabled}) {
    const [value, setValue] = useState ( "" );
    const [isFocused, setIsFocused] = useState(false);
    const textareaRef = useRef ( null );

    const handleSend = () => {
        const trimmed = value.trim ();
        if (!trimmed || isDisabled) return;
        onSend ( trimmed );
        setValue ( "" );
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault ();
            handleSend ();
        }
    };

    const handleChange = (e) => {
        setValue ( e.target.value );
        // Auto-resize
        const el = textareaRef.current;
        if (el) {
            el.style.height = "auto";
            el.style.height = Math.min ( el.scrollHeight, 160 ) + "px";
        }
    };

    const canSend = value.trim ().length > 0 && !isDisabled;

    return (
        <div
            style={{
                padding: "16px 0 8px",
                position: "relative",
                zIndex: 1,
            }}
        >
            {/* Input container */}
            <div
                onClick={() => textareaRef.current?.focus ()}
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    background: "var(--bg-input)",
                    backdropFilter: "blur(12px)",
                    WebkitBackdropFilter: "blur(12px)",
                    border: `1px solid ${
                        isFocused
                            ? "var(--accent-primary)"
                            : canSend
                            ? "var(--accent-dim)"
                            : "var(--border-subtle)"
                    }`,
                    borderRadius: "var(--radius-xl)",
                    padding: "13px 18px",
                    transition: "all var(--transition)",
                    boxShadow: isFocused
                        ? "0 0 0 3px var(--accent-glow), 0 8px 24px rgba(0, 0, 0, 0.12)"
                        : canSend
                        ? "0 0 20px rgba(99, 102, 241, 0.08)"
                        : "none",
                    cursor: "text",
                }}
            >
                <textarea
                    ref={textareaRef}
                    value={value}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    placeholder="Message Cyris..."
                    rows={1}
                    style={{
                        flex: 1,
                        width: "100%",
                        background: "transparent",
                        border: "none",
                        outline: "none",
                        resize: "none",
                        color: "var(--text-primary)",
                        fontFamily: "var(--font-sans)",
                        fontSize: "16px",
                        fontWeight: 400,
                        lineHeight: "1.6",
                        padding: 0,
                        margin: 0,
                        caretColor: "var(--accent-primary)",
                        minHeight: "26px",
                        maxHeight: "200px",
                        overflowY: "auto",
                        display: "block",
                    }}
                />

                {/* Send button */}
                <button
                    onClick={handleSend}
                    disabled={!canSend}
                    aria-label="Send message"
                    style={{
                        flexShrink: 0,
                        width: "34px",
                        height: "34px",
                        borderRadius: "50%",
                        border: canSend
                            ? "1px solid var(--accent-primary)"
                            : "1px solid var(--border-subtle)",
                        background: canSend
                            ? "var(--accent-primary)"
                            : "var(--bg-base)",
                        color: canSend
                            ? "#ffffff"
                            : "var(--text-muted)",
                        cursor: canSend ? "pointer" : "default",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        transition:
                            "background var(--transition), transform var(--transition), box-shadow var(--transition)",
                        boxShadow: canSend
                            ? "0 0 16px rgba(123, 108, 255, 0.4)"
                            : "none",
                        transform: canSend ? "scale(1)" : "scale(0.95)",
                    }}
                    onMouseEnter={(e) => {
                        if (canSend) {
                            e.currentTarget.style.transform = "scale(1.08)";
                        }
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.transform = canSend
                            ? "scale(1)"
                            : "scale(0.95)";
                    }}
                >
                    {/* Arrow up icon */}
                    <svg
                        width="15"
                        height="15"
                        viewBox="0 0 15 15"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M7.5 12V3M7.5 3L3.5 7M7.5 3L11.5 7"
                            stroke="currentColor"
                            strokeWidth="1.6"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </button>
            </div>

            {/* Hint text */}
            <p
                style={{
                    textAlign: "center",
                    fontSize: "11.5px",
                    color: "var(--text-muted)",
                    marginTop: "10px",
                    fontFamily: "var(--font-sans)",
                    letterSpacing: "0.02em",
                }}
            >
                Cyris is an AI assistant and can make mistakes.
            </p>
        </div>
    );
}