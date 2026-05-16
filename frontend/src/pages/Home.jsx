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
                title="System Coordination"
            >

                <SystemStatusBar
                    runtimeStatus={runtimeStatus}
                    interactionStatus={
                        interactionStatus
                    }
                />

                <InteractionStatusCard
                    status={interactionStatus}
                />

            </SectionContainer>

            <SectionContainer
                title="Adaptive Continuity"
            >

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

            </SectionContainer>

            <SectionContainer
                title="Orchestration Overview"
            >

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

            </SectionContainer>

            <SectionContainer
                title="Deployment Readiness"
            >

                <EnvironmentStatusCard
                    environmentStatus={
                        environmentStatus
                    }
                />

                <SystemHealthOverview
                    systemHealth={
                        systemHealth
                    }
                />

            </SectionContainer>

            <SectionContainer
                title="Validation Coordination"
            >

                <ValidationStatusCard
                    validationStatus={
                        validationStatus
                    }
                />

            </SectionContainer>

            <SectionContainer
                title="MVP Status"
            >

                <MVPStatusPanel
                    mvpState={mvpState}
                />

            </SectionContainer>

            <InteractionStatusCard
                status={interactionStatus}
            />

            <SystemOverview/>

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

        </div>
    );
}