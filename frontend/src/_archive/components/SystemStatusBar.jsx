export default function SystemStatusBar({
                                            runtimeStatus,
                                            interactionStatus
                                        }) {

    return (

        <div>

            <strong>
                Runtime:
            </strong>

            {" "}
            {runtimeStatus}

            {" | "}

            <strong>
                Interaction:
            </strong>

            {" "}
            {interactionStatus}

        </div>
    );
}