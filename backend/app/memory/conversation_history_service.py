import json
from pathlib import Path


class ConversationHistoryService:

    def __init__(self):
        self.file_path = Path(
            "data/conversation_history.json"
        )

    def load_history(self):
        with open(
                self.file_path,
                "r"
        ) as file:
            return json.load(file)

    def save_history(
            self,
            history
    ):
        with open(
                self.file_path,
                "w"
        ) as file:
            json.dump(
                history,
                file,
                indent=4
            )

    def add_message(
            self,
            role,
            content
    ):
        history = (
            self.load_history()
        )

        history[
            "messages"
        ].append(
            {
                "role": role,
                "content": content
            }
        )

        history[
            "messages"
        ] = history[
            "messages"
        ][-10:]

        self.save_history(
            history
        )

    def get_messages(self):
        history = (
            self.load_history()
        )

        return history[
            "messages"
        ]