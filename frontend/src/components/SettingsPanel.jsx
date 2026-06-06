import {useEffect} from "react";

export default function SettingsPanel({isOpen, onClose, currentTheme, onThemeChange}) {
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "";
        }
        return () => {
            document.body.style.overflow = "";
        };
    }, [isOpen]);

    return (
        <>
            {/* Backdrop Blur Overlay */}
            <div 
                className={`memory-overlay ${isOpen ? "open" : ""}`} 
                onClick={onClose}
            />

            {/* Sidebar Drawer */}
            <div className={`memory-drawer ${isOpen ? "open" : ""}`}>
                <div className="memory-header">
                    <div style={{display: "flex", flexDirection: "column", gap: "4px"}}>
                        <h2 style={{fontSize: "18px", fontWeight: 400, fontFamily: "var(--font-mono)", textTransform: "uppercase", letterSpacing: "0.08em"}}>
                            Settings
                        </h2>
                        <span style={{fontSize: "13px", color: "var(--text-muted)", fontFamily: "var(--font-sans)"}}>
                            Configure theme and visual options
                        </span>
                    </div>
                    <button 
                        onClick={onClose}
                        style={{
                            background: "transparent",
                            border: "none",
                            color: "var(--text-secondary)",
                            cursor: "pointer",
                            fontSize: "22px",
                            lineHeight: 1,
                            transition: "color var(--transition)"
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.color = "var(--text-primary)"}
                        onMouseLeave={(e) => e.currentTarget.style.color = "var(--text-secondary)"}
                    >
                        &times;
                    </button>
                </div>

                <div className="memory-content" style={{gap: "24px"}}>
                    <div style={{display: "flex", flexDirection: "column", gap: "12px"}}>
                        <span style={{fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--text-secondary)", textTransform: "uppercase", letterSpacing: "0.05em"}}>
                            Appearance
                        </span>
                        
                        <div style={{display: "flex", flexDirection: "column", gap: "12px"}}>
                            {/* Dark Mode Card */}
                            <div 
                                onClick={() => onThemeChange("dark")}
                                className="memory-card"
                                style={{
                                    cursor: "pointer",
                                    borderColor: currentTheme === "dark" ? "var(--accent-primary)" : "var(--border-subtle)",
                                    background: currentTheme === "dark" ? "var(--bg-elevated)" : "transparent",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "16px",
                                    padding: "16px"
                                }}
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
                                    style={{ color: currentTheme === "dark" ? "var(--accent-primary)" : "var(--text-secondary)" }}
                                >
                                    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
                                </svg>
                                <div style={{display: "flex", flexDirection: "column", gap: "4px", flex: 1}}>
                                    <span style={{fontSize: "14.5px", fontWeight: 400, color: "var(--text-primary)"}}>
                                        Dark Mode
                                    </span>
                                    <span style={{fontSize: "13px", color: "var(--text-muted)", lineHeight: "1.4"}}>
                                        Premium warm charcoal grey background
                                    </span>
                                </div>
                                {currentTheme === "dark" && (
                                    <div style={{
                                        width: "8px",
                                        height: "8px",
                                        borderRadius: "50%",
                                        background: "var(--accent-primary)",
                                        boxShadow: "0 0 8px var(--accent-primary)"
                                    }}/>
                                )}
                            </div>

                            {/* Light Mode Card */}
                            <div 
                                onClick={() => onThemeChange("light")}
                                className="memory-card"
                                style={{
                                    cursor: "pointer",
                                    borderColor: currentTheme === "light" ? "var(--accent-primary)" : "var(--border-subtle)",
                                    background: currentTheme === "light" ? "var(--bg-elevated)" : "transparent",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "16px",
                                    padding: "16px"
                                }}
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
                                    style={{ color: currentTheme === "light" ? "var(--accent-primary)" : "var(--text-secondary)" }}
                                >
                                    <circle cx="12" cy="12" r="4"/>
                                    <path d="M12 2v2"/>
                                    <path d="M12 20v2"/>
                                    <path d="m4.93 4.93 1.41 1.41"/>
                                    <path d="m17.66 17.66 1.41 1.41"/>
                                    <path d="M2 12h2"/>
                                    <path d="M20 12h2"/>
                                    <path d="m6.34 17.66-1.41 1.41"/>
                                    <path d="m19.07 4.93-1.41 1.41"/>
                                </svg>
                                <div style={{display: "flex", flexDirection: "column", gap: "4px", flex: 1}}>
                                    <span style={{fontSize: "14.5px", fontWeight: 400, color: "var(--text-primary)"}}>
                                        Light Mode
                                    </span>
                                    <span style={{fontSize: "13px", color: "var(--text-muted)", lineHeight: "1.4"}}>
                                        Clean warm-white Claude/ChatGPT style
                                    </span>
                                </div>
                                {currentTheme === "light" && (
                                    <div style={{
                                        width: "8px",
                                        height: "8px",
                                        borderRadius: "50%",
                                        background: "var(--accent-primary)",
                                        boxShadow: "0 0 8px var(--accent-primary)"
                                    }}/>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
