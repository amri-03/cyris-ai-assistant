import ResponseCard from "./ResponseCard";

export default function ConversationView({
                                             responses
                                         }) {

    return (
        <div>
            {
                responses.map (
                    (
                        response,
                        index
                    ) => (
                        <ResponseCard
                            key={index}
                            response={response}
                        />
                    )
                )
            }
        </div>
    );
}