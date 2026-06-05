import json
from pathlib import Path


class ConversationHistoryService:

    def __init__(self):
        self.file_path = Path(
            "data/conversation_history.json"
        )

    def load_history(self):
        try:
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Auto-create file if missing
            if not self.file_path.exists():
                default_history = {"messages": []}
                with open(self.file_path, "w") as file:
                    json.dump(default_history, file, indent=4)
                return default_history

            with open(
                    self.file_path,
                    "r"
            ) as file:
                return json.load(file)
        except Exception:
            return {"messages": []}

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