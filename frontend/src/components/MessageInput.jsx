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
                padding: "16px 0 24px",
                position: "relative",
                zIndex: 1,
            }}
        >
            {/* Input container */}
            <div
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
                    padding: "12px 16px",
                    transition: "border-color var(--transition)",
                    boxShadow: canSend
                        ? "0 0 24px rgba(123, 108, 255, 0.08)"
                        : "none",
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
                        background: "transparent",
                        border: "none",
                        outline: "none",
                        resize: "none",
                        color: "var(--text-primary)",
                        fontFamily: "var(--font-sans)",
                        fontSize: "14.5px",
                        fontWeight: 300,
                        lineHeight: "1.6",
                        caretColor: "var(--accent-primary)",
                        minHeight: "24px",
                        maxHeight: "160px",
                        overflowY: "auto",
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