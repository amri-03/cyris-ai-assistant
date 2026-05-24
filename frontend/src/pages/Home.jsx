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

import MVPStatusPanel
    from "../components/MVPStatusPanel";

import SectionContainer
    from "../components/SectionContainer";

import EnvironmentStatusCard
    from "../components/EnvironmentStatusCard";

import SystemHealthOverview
    from "../components/SystemHealthOverview";

import InteractionHeader
    from "../components/InteractionHeader";

import ValidationStatusCard
    from "../components/ValidationStatusCard";

import InteractionFooter
    from "../components/InteractionFooter";

import OperationalSummaryCard
    from "../components/OperationalSummaryCard";

import AdaptiveSystemBanner
    from "../components/AdaptiveSystemBanner";


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

    const mvpState =
        "adaptive_mvp_foundation_stable";

    const environmentStatus =
        "environment_ready";

    const systemHealth =
        "adaptive_system_stable";

    const interactionTitle =
        "Cyris Adaptive Interaction";

    const interactionSubtitle =
        "Continuity-aware adaptive orchestration environment.";

    const validationStatus =
        "adaptive_validation_stable";

    const operationalSummary =
        "Adaptive orchestration systems operating within stable MVP parameters.";

    const adaptiveBannerMessage =
        "Cyris is operating within stable adaptive coordination parameters.";

    return (
        <div>

            <h1>
                Cyris AI Assistant
            </h1>

            <InteractionHeader
                title={interactionTitle}
                subtitle={interactionSubtitle}
            />

            <SectionContainer
                title="Adaptive Interaction"
            >

                <InteractionTimeline
                    responses={responses}
                />

                <ConversationInput
                    onSend={handleSend}
                />

            </SectionContainer>

            <InteractionFooter/>

        </div>
    );
}