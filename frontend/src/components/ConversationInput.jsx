import {useState} from "react";

export default function ConversationInput({
                                              onSend
                                          }) {

    const [message, setMessage] = useState ( "" );

    const handleSend = () => {

        if (!message.trim ()) {
            return;
        }

        onSend ( message );

        setMessage ( "" );
    };

    return (
        <div className="flex flex-col gap-4">

            <textarea
                value={message}
                onChange={(event) =>
                    setMessage ( event.target.value )
                }
                placeholder="Interact with Cyris..."
                className="
                    w-full
                    min-h-[120px]
                    bg-neutral-900
                    border
                    border-neutral-800
                    rounded-2xl
                    px-4
                    py-4
                    text-white
                    resize-none
                    outline-none
                    focus:border-indigo-500
                "
            />

            <div className="flex justify-end">

                <button
                    onClick={handleSend}
                    className="
                        bg-indigo-500
                        hover:bg-indigo-400
                        transition
                        px-5
                        py-2.5
                        rounded-xl
                        text-sm
                        font-medium
                    "
                >
                    Send
                </button>

            </div>

        </div>
    );
}