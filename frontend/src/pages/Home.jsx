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
            className="
                min-h-screen
                bg-black
                text-white
                flex
                flex-col
            "
        >

            <div
                className="
                    w-full
                    border-b
                    border-neutral-900
                "
            >
                <div
                    className="
                        max-w-4xl
                        mx-auto
                        px-6
                        py-5
                    "
                >

                    <h1
                        className="
                            text-4xl
                            font-semibold
                            tracking-tight
                        "
                    >
                        Cyris
                    </h1>

                    <p
                        className="
                            text-neutral-500
                            mt-2
                            text-sm
                        "
                    >
                        Your adaptive assistant
                    </p>

                </div>
            </div>

            <div
                className="
                    flex-1
                    overflow-y-auto
                    px-6
                    py-8
                    max-w-4xl
                    w-full
                    mx-auto
                "
            >

                <InteractionTimeline
                    responses={responses}
                />

            </div>

            <div
                className="
                    border-t
                    border-neutral-900
                "
            >
                <div
                    className="
                        max-w-4xl
                        mx-auto
                        px-6
                        py-5
                    "
                >

                <ConversationInput
                    onSend={handleSend}
                />

                </div>
                
            </div>

        </div>
    );
}