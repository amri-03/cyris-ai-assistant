export default function BehaviorSummaryCard({
                                                summary
                                            }) {

    return (
        <div>

            <h3>
                Behavioral Summary
            </h3>

            <p>
                Engagement:
                {
                    summary.engagement_state
                }
            </p>

            <p>
                Focus:
                {
                    summary.focus_state
                }
            </p>

        </div>
    );
}