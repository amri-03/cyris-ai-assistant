import {useState} from "react";

import api from "../services/api";

import ConversationInput
    from "../components/ConversationInput";

import ConversationView
    from "../components/ConversationView";

import SystemOverview
    from "../components/SystemOverview";

import InteractionStatusCard
    from "../components/InteractionStatusCard";

import SystemStatusBar
    from "../components/SystemStatusBar";

import InteractionTimeline
    from "../components/InteractionTimeline";

import ContinuityPanel
    from "../components/ContinuityPanel";

import AdaptiveContextCard
    from "../components/AdaptiveContextCard";

import OrchestrationStateCard
    from "../components/OrchestrationStateCard";

import CoordinationOverview
    from "../components/CoordinationOverview";


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

    const runtimeStatus =
        "runtime_stable";

    const interactionStatus =
        "adaptive_interaction_active";

    const continuityState =
        "continuity_stable";

    const adaptiveContext =
        "Adaptive orchestration context active.";

    const orchestrationState =
        "adaptive_orchestration_stable";

    const coordinationOverview =
        "Runtime, behavioral, and AI coordination synchronized.";

    return (
        <div>

            <h1>
                Cyris AI Assistant
            </h1>

            <SystemStatusBar
                runtimeStatus={runtimeStatus}
                interactionStatus={
                    interactionStatus
                }
            />

            <ContinuityPanel
                continuityState={
                    continuityState
                }
            />

            <AdaptiveContextCard
                contextSummary={
                    adaptiveContext
                }
            />

            <OrchestrationStateCard
                orchestrationState={
                    orchestrationState
                }
            />

            <CoordinationOverview
                coordinationSummary={
                    coordinationOverview
                }
            />

            <InteractionStatusCard
                status={interactionStatus}
            />

            <SystemOverview/>

            <InteractionTimeline
                responses={responses}
            />

            <ConversationInput
                onSend={handleSend}
            />

        </div>
    );
}