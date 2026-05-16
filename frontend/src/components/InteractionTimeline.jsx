export default function InteractionTimeline({
                                                responses
                                            }) {

    return (

        <div>

            <h3>
                Interaction Timeline
            </h3>

            {
                responses.map (
                    (
                        response,
                        index
                    ) => (

                        <p key={index}>
                            {response}
                        </p>
                    )
                )
            }

        </div>
    );
}