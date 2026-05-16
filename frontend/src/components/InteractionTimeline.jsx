import AdaptiveResponseCard
    from "./AdaptiveResponseCard";


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

                        <AdaptiveResponseCard
                            key={index}
                            response={response}
                        />
                    )
                )
            }

        </div>
    );
}