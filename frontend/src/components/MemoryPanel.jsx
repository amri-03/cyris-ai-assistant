import {useEffect, useState} from "react";
import api from "../services/api";

export default function MemoryPanel({isOpen, onClose, items, onDelete, onReconcile}) {
    const [isReconciling, setIsReconciling] = useState(false);

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

    return (
        <>
            {/* Backdrop Overlay */}
            <div 
                className={`memory-overlay ${isOpen ? "open" : ""}`} 
                onClick={onClose}
            />

            {/* Center Modal Dialog */}
            <div className={`memory-modal ${isOpen ? "open" : ""}`}>
                <div className="memory-header">
                    <div style={{display: "flex", flexDirection: "column", gap: "4px"}}>
                        <h2 style={{fontSize: "18px", fontWeight: 400, fontFamily: "var(--font-mono)", textTransform: "uppercase", letterSpacing: "0.08em"}}>
                            Memory Profile
                        </h2>
                        <span style={{fontSize: "13px", color: "var(--text-muted)", fontFamily: "var(--font-sans)"}}>
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

                <div className="memory-content">
                    {/* Action Header */}
                    <div style={{display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px"}}>
                        <span style={{fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--text-secondary)", textTransform: "uppercase"}}>
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
                                fontSize: "12px",
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
                            <span style={{fontSize: "28px", marginBottom: "12px"}}>🔮</span>
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
        </>
    );
}
