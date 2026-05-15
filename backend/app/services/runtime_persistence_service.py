import json
from pathlib import Path


class RuntimePersistenceService:

    def __init__(self):
        self.storage_path = Path(
            "data/runtime_history.json"
        )

    def save_runtime_history(
            self,
            history
    ):
        serialized = [
            item.model_dump(mode="json")
            for item in history
        ]

        with open(self.storage_path, "w") as file:
            json.dump(
                serialized,
                file,
                indent=4
            )

    def load_runtime_history(self):
        with open(
                self.storage_path,
                "r"
        ) as file:
            return json.load(file)