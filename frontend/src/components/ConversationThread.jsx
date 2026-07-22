import MessageBubble from "./MessageBubble";
import ThinkingIndicator from "./ThinkingIndicator";

const starterCards = [
    {
        title: "Talk about what's on your mind",
        subtitle: "Share your thoughts, feelings, or recent experiences in a supportive space.",
        prompt: "I'd like to talk about what's on my mind today.",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
        )
    },
    {
        title: "Pick up where we left off",
        subtitle: "Review your ongoing goals, recent behavioral insights, or past reflections.",
        prompt: "Let's pick up where we left off in our previous conversation.",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
            </svg>
        )
    },
    {
        title: "Help me plan my next steps",
        subtitle: "Break down goals into manageable actions and build healthy daily habits.",
        prompt: "Can you help me plan actionable next steps for my current goal?",
        icon: (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
            </svg>
        )
    }
];

export default function ConversationThread({ messages, isThinking, onScrollToBottom, onSendStarter }) {
    const isEmpty = messages.length === 0 && !isThinking;

    return (
        <div className="thread-inner">
            {isEmpty ? (
                <div className="empty-state-container">
                    <div className="empty-state-header">
                        <div className="empty-state-avatar">
                            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
                                <path d="M12 12 2.1 7.1" />
                                <path d="m12 12 7.1-7.1" />
                            </svg>
                        </div>
                        <h1 className="empty-state-title">
                            Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"}
                        </h1>
                        <p className="empty-state-subtitle">How can Cyris support you today?</p>
                    </div>

                    <div className="starter-cards-grid">
                        {starterCards.map((card, idx) => (
                            <div
                                key={idx}
                                onClick={() => onSendStarter?.(card.prompt)}
                                className="starter-card-item"
                                tabIndex={0}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter" || e.key === " ") {
                                        e.preventDefault();
                                        onSendStarter?.(card.prompt);
                                    }
                                }}
                            >
                                <div className="starter-card-title">
                                    {card.icon}
                                    <span>{card.title}</span>
                                </div>
                                <div className="starter-card-desc">{card.subtitle}</div>
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
                <>
                    {messages.map((msg, index) => (
                        <MessageBubble
                            key={index}
                            role={msg.role}
                            content={msg.content}
                            isLatest={index === messages.length - 1}
                            onScrollToBottom={onScrollToBottom}
                            animate={msg.animate}
                            feedback={msg.feedback}
                        />
                    ))}

                    {isThinking && <ThinkingIndicator />}
                </>
            )}
        </div>
    );
}