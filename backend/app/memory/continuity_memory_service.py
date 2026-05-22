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

        existing_item = None

        for item in memory[
            "continuity_items"
        ]:

            if (
                    item["content"]
                    == extracted["content"]
            ):
                existing_item = item
                break

        if existing_item:

            existing_item["priority"] += 1

        else:

            memory[
                "continuity_items"
            ].append(
                {
                    "content":
                        extracted["content"],

                    "topics":
                        extracted["topics"],

                    "priority": 1
                }
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

        items = sorted(
            memory[
                "continuity_items"
            ],
            key=lambda item:
            item["priority"],
            reverse=True
        )[:10]

        if not items:
            return ""

        formatted = "\n".join(
            [
                item["content"]
                for item in items
            ]
        )

        return (
            "Known user continuity:\n"
            f"{formatted}"
        )