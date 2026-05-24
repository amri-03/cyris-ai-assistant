import AdaptiveResponseCard
    from "./AdaptiveResponseCard";


export default function InteractionTimeline({
                                                responses
                                            }) {

    return (

        <div className="flex flex-col gap-4">

            {responses.map (
                (message, index) => {

                    const isUser =
                        message.startsWith ( "User:" );

                    return (

                        <div
                            key={index}
                            className={
                                `flex ${
                                    isUser
                                        ? "justify-end"
                                        : "justify-start"
                                }`
                            }
                        >

                            <div
                                className={
                                    `
                            max-w-[75%]
                            px-4
                            py-3
                            rounded-2xl
                            whitespace-pre-wrap
                            text-sm
                            leading-relaxed
                            ${
                                        isUser
                                            ? "bg-indigo-600 text-white"
                                            : "bg-neutral-900 text-neutral-100"
                                    }
                            `
                                }
                            >

                                {
                                    message.replace (
                                        /^User:\s?|^Cyris:\s?/,
                                        ""
                                    )
                                }

                            </div>

                        </div>
                    );
                }
            )}

        </div>
    );
}