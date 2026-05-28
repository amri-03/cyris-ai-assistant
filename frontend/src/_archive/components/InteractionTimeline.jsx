import {useEffect, useRef} from "react";

export default function InteractionTimeline({
    responses
}) {

    const bottomRef = useRef ( null );

    useEffect ( () => {
        bottomRef.current?.scrollIntoView ( {
            behavior: "smooth",
        } );
    }, [responses] );


    if (responses.length === 0) {
        return (
            <div
                className="
                    text-neutral-600
                    text-sm
                    pt-10
                "
            >
                Start a conversation with Cyris.
            </div>
        );
    }

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
                            max-w-[70%]
                            px-4
                            py-3
                            rounded-3xl
                            whitespace-pre-wrap
                            text-[15px]
                            leading-relaxed
                            ${
                                        isUser
                                            ? "bg-indigo-500 text-white"
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

            <div ref={bottomRef}/>

        </div>

    );
}