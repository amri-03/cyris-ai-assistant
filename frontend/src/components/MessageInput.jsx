import {useState, useRef} from "react";

export default function MessageInput({onSend, isDisabled}) {
    const [value, setValue] = useState ( "" );
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
                    alignItems: "flex-end",
                    gap: "12px",
                    background: "var(--bg-input)",
                    border: `1px solid ${
                        canSend
                            ? "var(--accent-dim)"
                            : "var(--border-subtle)"
                    }`,
                    borderRadius: "var(--radius-xl)",
                    padding: "13px 18px",
                    transition: "border-color var(--transition)",
                    boxShadow: canSend
                        ? "0 0 24px rgba(123, 108, 255, 0.08)"
                        : "none",
                    cursor: "text",
                }}
            >
                <textarea
                    ref={textareaRef}
                    value={value}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
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
                        fontWeight: 300,
                        lineHeight: "1.6",
                        padding: 0,
                        margin: 0,
                        caretColor: "var(--accent-primary)",
                        minHeight: "24px",
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
                        border: "none",
                        background: canSend
                            ? "var(--accent-primary)"
                            : "var(--bg-elevated)",
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
                    fontSize: "11px",
                    color: "var(--text-muted)",
                    marginTop: "10px",
                    fontFamily: "var(--font-mono)",
                    letterSpacing: "0.05em",
                }}
            >
                Enter to send · Shift+Enter for new line
            </p>
        </div>
    );
}