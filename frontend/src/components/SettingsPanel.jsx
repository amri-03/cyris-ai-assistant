import { useEffect } from "react";
import { createPortal } from "react-dom";

export default function SettingsPanel({ isOpen, onClose, currentTheme, onThemeChange }) {
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            if (e.key === "Escape") {
                onClose();
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return createPortal(
        <div className="modal-portal-wrapper">
            <div className={`modal-overlay ${isOpen ? "modal-overlay-open" : ""}`} onClick={onClose} />

            <div className={`modal-card modal-card-settings ${isOpen ? "modal-card-open" : ""}`}>
                <div className="modal-header">
                    <div className="modal-header-titles">
                        <h2 className="modal-title">Settings</h2>
                        <span className="modal-subtitle">Configure theme and visual preference</span>
                    </div>
                    <button onClick={onClose} className="modal-close-btn" aria-label="Close settings">
                        &times;
                    </button>
                </div>

                <div className="modal-body">
                    <span className="settings-section-label">Appearance</span>

                    {/* Dark Mode Card */}
                    <div
                        onClick={() => onThemeChange("dark")}
                        tabIndex={0}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                onThemeChange("dark");
                            }
                        }}
                        className={`theme-option-card ${currentTheme === "dark" ? "selected" : ""}`}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="theme-icon"
                        >
                            <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
                        </svg>
                        <div className="theme-info">
                            <span className="theme-name">Dark Mode</span>
                            <span className="theme-desc">Obsidian & slate dark theme</span>
                        </div>
                        {currentTheme === "dark" && <div className="theme-radio-dot" />}
                    </div>

                    {/* Light Mode Card */}
                    <div
                        onClick={() => onThemeChange("light")}
                        tabIndex={0}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                onThemeChange("light");
                            }
                        }}
                        className={`theme-option-card ${currentTheme === "light" ? "selected" : ""}`}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="theme-icon"
                        >
                            <circle cx="12" cy="12" r="4" />
                            <path d="M12 2v2" />
                            <path d="M12 20v2" />
                            <path d="m4.93 4.93 1.41 1.41" />
                            <path d="m17.66 17.66 1.41 1.41" />
                            <path d="M2 12h2" />
                            <path d="M20 12h2" />
                            <path d="m6.34 17.66-1.41 1.41" />
                            <path d="m19.07 4.93-1.41 1.41" />
                        </svg>
                        <div className="theme-info">
                            <span className="theme-name">Light Mode</span>
                            <span className="theme-desc">Chalk & river silt light theme</span>
                        </div>
                        {currentTheme === "light" && <div className="theme-radio-dot" />}
                    </div>
                </div>
            </div>
        </div>,
        document.body
    );
}
