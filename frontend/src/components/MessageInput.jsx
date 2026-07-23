import { useState, useRef } from "react";

export default function MessageInput({ onSend, isDisabled }) {
    const [value, setValue] = useState("");
    const [isFocused, setIsFocused] = useState(false);
    const textareaRef = useRef(null);

    const handleSend = () => {
        const trimmed = value.trim();
        if (!trimmed || isDisabled) return;
        onSend(trimmed);
        setValue("");
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleChange = (e) => {
        setValue(e.target.value);
        const el = textareaRef.current;
        if (el) {
            el.style.height = "auto";
            el.style.height = `${Math.min(el.scrollHeight, 180)}px`;
        }
    };

    const canSend = value.trim().length > 0 && !isDisabled;

    return (
        <div className="input-fixed-wrapper">
            <div className="input-inner-container">
                <div
                    onClick={() => textareaRef.current?.focus()}
                    className={`input-box ${isFocused ? "input-box-focused" : canSend ? "input-box-active" : ""}`}
                >
                    <textarea
                        ref={textareaRef}
                        value={value}
                        onChange={handleChange}
                        onKeyDown={handleKeyDown}
                        onFocus={() => setIsFocused(true)}
                        onBlur={(e) => {
                            // Only blur if the user clicked outside the input container
                            setIsFocused(false);
                        }}
                        readOnly={isDisabled}
                        placeholder="Message Cyris..."
                        rows={1}
                        className="input-textarea"
                    />

                    <button
                        onClick={handleSend}
                        disabled={!canSend}
                        aria-label="Send message"
                        className={`btn-send ${canSend ? "btn-send-active" : ""}`}
                    >
                        <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
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

                <p className="input-footer-hint">Cyris is an AI assistant and can make mistakes.</p>
            </div>
        </div>
    );
}