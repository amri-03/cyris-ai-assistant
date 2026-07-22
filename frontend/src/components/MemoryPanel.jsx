import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import api from "../services/api";

export default function MemoryPanel({ isOpen, onClose }) {
    const [memoryItems, setMemoryItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchMemory = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const res = await api.get("/memory-status");
            const items = res.data?.continuity_items || (Array.isArray(res.data) ? res.data : []);
            setMemoryItems(items);
        } catch (err) {
            console.error("Failed to fetch memory status", err);
            setError("Unable to load continuity memory.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchMemory();
        }
    }, [isOpen]);

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

    const handleDelete = async (identity) => {
        if (!identity) return;
        try {
            await api.delete(`/memory/${encodeURIComponent(identity)}`);
            setMemoryItems((prev) => prev.filter((item) => (item.identity || item.id) !== identity));
        } catch (err) {
            console.error("Failed to delete memory item", err);
        }
    };

    if (!isOpen) return null;

    return createPortal(
        <div className="modal-portal-wrapper">
            <div className={`modal-overlay ${isOpen ? "modal-overlay-open" : ""}`} onClick={onClose} />
            
            <div className={`modal-card ${isOpen ? "modal-card-open" : ""}`}>
                <div className="modal-header">
                    <div className="modal-header-titles">
                        <h2 className="modal-title">Continuity Memory</h2>
                        <span className="modal-subtitle">Stored identity facts & background context</span>
                    </div>
                    <button onClick={onClose} className="modal-close-btn" aria-label="Close modal">
                        &times;
                    </button>
                </div>

                <div className="modal-body">
                    {isLoading ? (
                        <div className="memory-empty-state">Loading continuity memory...</div>
                    ) : error ? (
                        <div className="memory-empty-state">{error}</div>
                    ) : memoryItems.length === 0 ? (
                        <div className="memory-empty-state">No continuity memory items recorded yet.</div>
                    ) : (
                        memoryItems.map((item, idx) => {
                            const identity = item.identity || item.id || `item-${idx}`;
                            const itemType = item.type || "context";
                            const importance = item.importance || "normal";

                            return (
                                <div key={identity} className="memory-card">
                                    <div className="memory-card-top">
                                        <span className={`memory-type-badge ${itemType}`}>{itemType}</span>
                                        <button
                                            onClick={() => handleDelete(identity)}
                                            className="memory-delete-btn"
                                            title="Delete memory item"
                                        >
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M3 6h18" />
                                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                            </svg>
                                        </button>
                                    </div>

                                    <p className="memory-card-content">{item.content || item.value || JSON.stringify(item)}</p>

                                    <div className="memory-card-meta">
                                        <span>id: {identity}</span>
                                        <span>importance: {importance}</span>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>
        </div>,
        document.body
    );
}
