import {useState} from "react";

import api from "../services/api";

import ConversationInput
    from "../components/ConversationInput";

import ConversationView
    from "../components/ConversationView";

import SystemOverview
    from "../components/SystemOverview";


export default function Home() {

    const [responses, setResponses] =
        useState ( [] );

    const handleSend = async (
        message
    ) => {

        try {

            const response =
                await api.get (
                    "/ai-test"
                );

            const content =
                response.data.response?.content
                ||
                response.data.error
                ||
                "No response available.";

            setResponses (
                (previous) => [
                    ...previous,
                    `User: ${message}`,
                    `Cyris: ${content}`
                ]
            );

        } catch (error) {

            setResponses (
                (previous) => [
                    ...previous,
                    "Cyris: Backend connection failed."
                ]
            );
        }
    };

    return (
        <div>

            <h1>
                Cyris AI Assistant
            </h1>

            <SystemOverview/>

            <ConversationView
                responses={responses}
            />

            <ConversationInput
                onSend={handleSend}
            />

        </div>
    );
}