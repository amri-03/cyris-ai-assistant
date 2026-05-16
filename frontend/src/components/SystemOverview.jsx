import RuntimeSummaryCard
    from "./RuntimeSummaryCard";

import BehaviorSummaryCard
    from "./BehaviorSummaryCard";


export default function SystemOverview() {

    const runtimeSummary = {
        runtime_status:
            "runtime_stable",

        coordination_state:
            "adaptive_orchestration_active"
    };

    const behavioralSummary = {
        engagement_state:
            "engaged",

        focus_state:
            "stable_focus"
    };

    return (
        <div>

            <RuntimeSummaryCard
                summary={runtimeSummary}
            />

            <BehaviorSummaryCard
                summary={behavioralSummary}
            />

        </div>
    );
}