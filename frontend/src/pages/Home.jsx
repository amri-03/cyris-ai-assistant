import {useState} from "react";

import api from "../services/api";

import ConversationInput
    from "../components/ConversationInput";

import InteractionTimeline
    from "../components/InteractionTimeline";


export default function Home() {

    const [responses, setResponses] =
        useState ( [] );

    const handleSend = async (
        message
    ) => {

        try {

            const response =
                await api.post (
                    "/ai-test",
                    {prompt: message}
                );

            const content =
                response.data.response?.response
                ||
                response.data.response?.error
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
        <div
            className="min-h-screen bg-black text-white flex flex-col"
        >

            <div
                className="px-6 py-6 border-b border-neutral-800"
            >

                <h1
                    className="text-3xl font-semibold"
                >
                    Cyris
                </h1>

                <p
                    className="text-neutral-400 mt-1"
                >
                    Your adaptive assistant
                </p>

            </div>

            <div
                className="flex-1 overflow-y-auto px-6 py-6"
            >

                <InteractionTimeline
                    responses={responses}
                />

            </div>

            <div
                className="border-t border-neutral-800 px-6 py-4"
            >

                <ConversationInput
                    onSend={handleSend}
                />

            </div>

        </div>
    );
}