import json
from pathlib import Path

from app.memory.continuity_extractor import (
    ContinuityExtractor
)


class ContinuityMemoryService:

    def __init__(self):

        self.memory_file = (
            Path(
                "data/user_continuity.json"
            )
        )

        self.extractor = (
            ContinuityExtractor()
        )

    def load_memory(self):

        try:

            with open(
                    self.memory_file,
                    "r"
            ) as file:

                return json.load(file)

        except Exception:

            return {
                "continuity_items": []
            }

    def save_continuity(
            self,
            message: str
    ):

        extracted = (
            self.extractor
            .extract_continuity(
                message
            )
        )

        if not extracted:
            return

        memory = (
            self.load_memory()
        )

        if (
                extracted
                not in memory[
            "continuity_items"
        ]
        ):
            memory[
                "continuity_items"
            ].append(
                extracted
            )

        with open(
                self.memory_file,
                "w"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4
            )

    def build_continuity_context(self):

        memory = (
            self.load_memory()
        )

        items = (
            memory[
                "continuity_items"
            ][-10:]
        )

        if not items:
            return ""

        formatted = "\n".join(items)

        return (
            "Known user continuity:\n"
            f"{formatted}"
        )