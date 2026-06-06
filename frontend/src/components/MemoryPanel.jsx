import {useState} from "react";
import {createPortal} from "react-dom";
import api from "../services/api";

export default function MemoryPanel({isOpen, onClose, items, onDelete, onReconcile}) {
    const [isReconciling, setIsReconciling] = useState(false);

    const handleReconcile = async () => {
        setIsReconciling(true);
        try {
            await api.post("/memory/reconcile");
            if (onReconcile) {
                await onReconcile();
            }
        } catch (error) {
            console.error("Failed to reconcile memory", error);
        } finally {
            setIsReconciling(false);
        }
    };

    const formatDate = (isoString) => {
        if (!isoString) return "n/a";
        try {
            const date = new Date(isoString);
            return date.toLocaleDateString(undefined, {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            });
        } catch {
            return "n/a";
        }
    };

    return createPortal(
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none", zIndex: 99999 }}>
            {/* Backdrop Overlay */}
            <div 
                className={`memory-overlay ${isOpen ? "open" : ""}`} 
                onClick={onClose}
                style={{ zIndex: 10000, pointerEvents: isOpen ? "auto" : "none" }}
            />

            {/* Center Modal Dialog */}
            <div className={`memory-modal ${isOpen ? "open" : ""}`} style={{ zIndex: 10001, pointerEvents: "auto" }}>
                <div className="memory-header">
                    <div style={{display: "flex", flexDirection: "column", gap: "4px"}}>
                        <h2 style={{fontSize: "22px", fontWeight: 400, fontFamily: "var(--font-mono)", textTransform: "uppercase", letterSpacing: "0.08em"}}>
                            Memory Profile
                        </h2>
                        <span style={{fontSize: "14.5px", color: "var(--text-muted)", fontFamily: "var(--font-sans)"}}>
                            Remembered context for this session
                        </span>
                    </div>
                    <button 
                        onClick={onClose}
                        style={{
                            background: "transparent",
                            border: "none",
                            color: "var(--text-secondary)",
                            cursor: "pointer",
                            fontSize: "26px",
                            lineHeight: 1,
                            transition: "color var(--transition)"
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.color = "var(--text-primary)"}
                        onMouseLeave={(e) => e.currentTarget.style.color = "var(--text-secondary)"}
                    >
                        &times;
                    </button>
                </div>

                <div className="memory-content">
                    {/* Action Header */}
                    <div style={{display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px"}}>
                        <span style={{fontFamily: "var(--font-mono)", fontSize: "13.5px", color: "var(--text-secondary)", textTransform: "uppercase"}}>
                            {items.length} items active
                        </span>
                        <button
                            onClick={handleReconcile}
                            disabled={isReconciling || items.length === 0}
                            style={{
                                background: "transparent",
                                border: "1px solid var(--border-subtle)",
                                borderRadius: "4px",
                                padding: "6px 12px",
                                fontSize: "13px",
                                fontFamily: "var(--font-mono)",
                                textTransform: "uppercase",
                                color: "var(--text-secondary)",
                                cursor: items.length > 0 ? "pointer" : "not-allowed",
                                opacity: items.length > 0 ? 1 : 0.5,
                                transition: "all var(--transition)"
                            }}
                            onMouseEnter={(e) => {
                                if (items.length > 0) {
                                    e.currentTarget.style.borderColor = "var(--user-border)";
                                    e.currentTarget.style.color = "var(--text-primary)";
                                    e.currentTarget.style.background = "var(--bg-elevated)";
                                }
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = "var(--border-subtle)";
                                e.currentTarget.style.color = "var(--text-secondary)";
                                e.currentTarget.style.background = "transparent";
                            }}
                        >
                            {isReconciling ? "cleaning..." : "reconcile"}
                        </button>
                    </div>

                    {items.length === 0 ? (
                        <div style={{
                            flex: 1,
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                            color: "var(--text-muted)",
                            textAlign: "center",
                            padding: "40px 20px"
                        }}>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="36"
                                height="36"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                style={{ color: "var(--text-muted)", marginBottom: "16px" }}
                            >
                                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/>
                                <path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5Z"/>
                                <path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1Z"/>
                            </svg>
                            <p style={{fontSize: "14.5px", fontWeight: 300, lineHeight: 1.6}}>
                                No long-term continuity items stored yet. Chat with Cyris to populate memory.
                            </p>
                        </div>
                    ) : (
                        items.map((item) => (
                            <div className="memory-card" key={item.identity}>
                                <div className="memory-card-header">
                                    <span className={`memory-badge ${item.type || ""}`}>
                                        {(item.type || "interest").replace("_", " ")}
                                    </span>
                                    <button 
                                        className="memory-btn-delete"
                                        onClick={() => onDelete(item.identity)}
                                        title="Forget this info"
                                    >
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <polyline points="3 6 5 6 21 6"></polyline>
                                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                        </svg>
                                    </button>
                                </div>
                                <div className="memory-card-body">
                                    {item.content}
                                </div>
                                <div className="memory-card-footer">
                                    <span>priority: {item.priority || 3}</span>
                                    <span>
                                        {item.last_updated ? formatDate(item.last_updated) : "historical"}
                                    </span>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>,
        document.body
    );
}
