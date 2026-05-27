export default function RuntimeSummaryCard({
                                               summary
                                           }) {

    return (
        <div>

            <h3>
                Runtime Summary
            </h3>

            <p>
                Runtime Status:
                {
                    summary.runtime_status
                }
            </p>

            <p>
                Coordination State:
                {
                    summary.coordination_state
                }
            </p>

        </div>
    );
}