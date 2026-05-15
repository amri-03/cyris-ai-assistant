import json
from pathlib import Path


class SessionPersistenceService:

    def __init__(self):
        self.storage_path = Path(
            "data/session_state.json"
        )

    def save_session_state(
            self,
            state
    ):
        with open(
                self.storage_path,
                "w"
        ) as file:
            json.dump(
                state.model_dump(mode="json"),
                file,
                indent=4
            )

    def load_session_state(self):
        with open(
                self.storage_path,
                "r"
        ) as file:
            return json.load(file)