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
        <div>
            <textarea
                value={message}
                onChange={(event) =>
                    setMessage (
                        event.target.value
                    )
                }
                placeholder="Interact with Cyris..."
            />

            <button onClick={handleSend}>
                Send
            </button>
        </div>
    );
}