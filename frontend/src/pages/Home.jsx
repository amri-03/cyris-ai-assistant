import {useState} from "react";
import api from "../services/api";
import Header from "../components/Header";
import ConversationThread from "../components/ConversationThread";
import MessageInput from "../components/MessageInput";

export default function Home() {
    const [messages, setMessages] = useState ( [] );
    const [isThinking, setIsThinking] = useState ( false );
    const [isConnected, setIsConnected] = useState ( true );

    const handleSend = async (text) => {
        // Optimistically add user message
        const userMessage = {role: "user", content: text};
        setMessages ( (prev) => [...prev, userMessage] );
        setIsThinking ( true );

        try {
            const response = await api.post ( "/ai-test", {
                prompt: text,
            } );

            const content =
                response.data.response?.response ||
                response.data.response?.error ||
                "No response available.";

            setMessages ( (prev) => [
                ...prev,
                {role: "assistant", content},
            ] );

            setIsConnected ( true );
        } catch (error) {
            setMessages ( (prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "I wasn't able to reach the backend. Please check that the server is running.",
                },
            ] );
            setIsConnected ( false );
        } finally {
            setIsThinking ( false );
        }
    };

    return (
        <div
            style={{
                height: "100vh",
                display: "flex",
                flexDirection: "column",
                background: "var(--bg-base)",
                position: "relative",
            }}
        >
            {/* Constrained content column */}
            <div
                style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    width: "100%",
                    maxWidth: "720px",
                    margin: "0 auto",
                    padding: "0 24px",
                    minHeight: 0,
                }}
            >
                <Header isConnected={isConnected}/>

                <ConversationThread
                    messages={messages}
                    isThinking={isThinking}
                />

                <MessageInput
                    onSend={handleSend}
                    isDisabled={isThinking}
                />
            </div>
        </div>
    );
}