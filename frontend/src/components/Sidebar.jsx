import React, { useState } from 'react';

export default function Sidebar({
    isOpen,
    sessions,
    activeSessionId,
    onSelectSession,
    onNewChat,
    onDeleteSession,
    onToggleSidebar
}) {
    // Group sessions by date
    const groupSessions = (sessionsList) => {
        const groups = {
            'Today': [],
            'Previous 7 Days': [],
            'Older': []
        };
        
        const now = new Date();
        const todayStr = now.toDateString();
        
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(now.getDate() - 7);
        
        sessionsList.forEach(session => {
            const updated = new Date(session.updated_at);
            if (updated.toDateString() === todayStr) {
                groups['Today'].push(session);
            } else if (updated > sevenDaysAgo) {
                groups['Previous 7 Days'].push(session);
            } else {
                groups['Older'].push(session);
            }
        });
        
        return groups;
    };

    const groupedSessions = groupSessions(sessions || []);
    const [hoveredSessionId, setHoveredSessionId] = useState(null);
    const [menuOpenForId, setMenuOpenForId] = useState(null);

    const handleDeleteClick = (e, sessionId) => {
        e.stopPropagation();
        onDeleteSession(sessionId);
        setMenuOpenForId(null);
    };

    const toggleMenu = (e, sessionId) => {
        e.stopPropagation();
        setMenuOpenForId(prev => prev === sessionId ? null : sessionId);
    };

    const SessionItem = ({ session }) => {
        const isActive = activeSessionId === session.id;
        const isHovered = hoveredSessionId === session.id;
        const isMenuOpen = menuOpenForId === session.id;
        
        return (
            <div 
                onClick={() => onSelectSession(session.id)}
                onMouseEnter={() => setHoveredSessionId(session.id)}
                onMouseLeave={() => {
                    setHoveredSessionId(null);
                    if (!isMenuOpen) setMenuOpenForId(null);
                }}
                style={{
                    padding: '10px 14px',
                    margin: '3px 12px',
                    borderRadius: 'var(--radius-sm)',
                    cursor: 'pointer',
                    background: isActive 
                        ? 'var(--bg-elevated)' 
                        : isHovered 
                        ? 'rgba(99, 102, 241, 0.05)' 
                        : 'transparent',
                    borderLeft: isActive ? '3px solid var(--accent-primary)' : '3px solid transparent',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    transition: 'all var(--transition)',
                    position: 'relative'
                }}
            >
                <div style={{
                    color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                    fontSize: '13.5px',
                    fontWeight: isActive ? 500 : 400,
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    flex: 1,
                    fontFamily: 'var(--font-sans)',
                    paddingLeft: isActive ? '2px' : '5px'
                }}>
                    {session.title || 'New Chat'}
                </div>
                
                {/* Options Menu Button (...) */}
                {(isHovered || isMenuOpen) && (
                    <div 
                        onClick={(e) => toggleMenu(e, session.id)}
                        style={{
                            padding: '4px',
                            color: 'var(--text-muted)',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            borderRadius: '4px',
                            transition: 'color var(--transition)'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.color = 'var(--text-primary)'}
                        onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="1"></circle>
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </div>
                )}
                
                {/* Dropdown Menu */}
                {isMenuOpen && (
                    <div style={{
                        position: 'absolute',
                        right: '12px',
                        top: '32px',
                        background: 'var(--bg-drawer)',
                        backdropFilter: 'blur(16px)',
                        WebkitBackdropFilter: 'blur(16px)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '4px 0',
                        boxShadow: 'var(--shadow-modal)',
                        zIndex: 150,
                        minWidth: '130px'
                    }}>
                        <div 
                            onClick={(e) => handleDeleteClick(e, session.id)}
                            style={{
                                padding: '8px 12px',
                                color: '#ef4444',
                                fontSize: '12.5px',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                fontFamily: 'var(--font-sans)',
                                transition: 'background var(--transition)'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.08)'}
                            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                        >
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M3 6h18"></path>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                            Delete Chat
                        </div>
                    </div>
                )}
            </div>
        );
    };

    return (
        <div style={{
            width: isOpen ? '260px' : '0px',
            height: '100%',
            background: 'var(--bg-surface)',
            borderRight: isOpen ? '1px solid var(--border-subtle)' : 'none',
            transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            overflowX: 'hidden',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            flexShrink: 0,
            position: 'relative'
        }}>
            {isOpen && (
                <>
                    {/* Logo & Toggle Header */}
                    <div style={{
                        padding: '16px 16px 12px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        position: 'sticky',
                        top: 0,
                        background: 'var(--bg-surface)',
                        zIndex: 10
                    }}>
                        {/* Branding */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{
                                fontFamily: 'var(--font-mono)',
                                fontSize: '18px',
                                fontWeight: 600,
                                letterSpacing: '0.1em',
                                textTransform: 'uppercase',
                                color: 'var(--text-primary)'
                            }}>
                                Cyris
                            </span>
                            <span style={{
                                fontFamily: 'var(--font-mono)',
                                fontSize: '10px',
                                fontWeight: 300,
                                letterSpacing: '0.1em',
                                textTransform: 'uppercase',
                                color: 'var(--text-muted)',
                                background: 'var(--bg-elevated)',
                                padding: '1px 6px',
                                borderRadius: '99px',
                                border: '1px solid var(--border-subtle)'
                            }}>
                                active
                            </span>
                        </div>
                        
                        {/* Close Sidebar Toggle */}
                        <div 
                            onClick={onToggleSidebar}
                            style={{
                                padding: '8px',
                                cursor: 'pointer',
                                color: 'var(--text-secondary)',
                                borderRadius: 'var(--radius-sm)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                transition: 'all var(--transition)'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.background = 'var(--bg-elevated)';
                                e.currentTarget.style.color = 'var(--text-primary)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.color = 'var(--text-secondary)';
                            }}
                            title="Close sidebar"
                        >
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="9" y1="3" x2="9" y2="21"></line>
                            </svg>
                        </div>
                    </div>

                    {/* New Chat Action Button */}
                    <div style={{ padding: '0 16px 16px' }}>
                        <button
                            onClick={onNewChat}
                            style={{
                                width: '100%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px',
                                background: 'transparent',
                                border: '1px solid var(--border-subtle)',
                                color: 'var(--text-primary)',
                                padding: '10px 16px',
                                borderRadius: 'var(--radius-sm)',
                                cursor: 'pointer',
                                fontSize: '13.5px',
                                fontWeight: 500,
                                fontFamily: 'var(--font-sans)',
                                transition: 'all var(--transition)'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.background = 'var(--accent-glow)';
                                e.currentTarget.style.borderColor = 'var(--accent-primary)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.borderColor = 'var(--border-subtle)';
                            }}
                        >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                            New Chat
                        </button>
                    </div>

                    {/* Session Groups */}
                    <div style={{ 
                        flex: 1, 
                        overflowY: 'auto', 
                        paddingBottom: '20px',
                        paddingTop: '8px'
                    }}>
                        {Object.entries(groupedSessions).map(([groupName, groupSessions]) => {
                            if (groupSessions.length === 0) return null;
                            return (
                                <div key={groupName} style={{ marginBottom: '20px' }}>
                                    <div style={{
                                        padding: '0 20px 6px',
                                        fontSize: '11px',
                                        fontWeight: 600,
                                        color: 'var(--text-muted)',
                                        letterSpacing: '0.08em',
                                        textTransform: 'uppercase',
                                        fontFamily: 'var(--font-mono)'
                                    }}>
                                        {groupName}
                                    </div>
                                    {groupSessions.map(session => (
                                        <SessionItem key={session.id} session={session} />
                                    ))}
                                </div>
                            );
                        })}
                        {sessions.length === 0 && (
                            <div style={{
                                padding: '40px 20px',
                                textAlign: 'center',
                                color: 'var(--text-muted)',
                                fontSize: '13px',
                                fontFamily: 'var(--font-sans)'
                            }}>
                                No previous chats found.
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );
}
