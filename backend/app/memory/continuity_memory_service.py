import json
from pathlib import Path

from app.services.ai.continuity_ai_extractor import (
    ContinuityAIExtractor
)


class ContinuityMemoryService:

    def __init__(self):

        self.memory_file = (
            Path(
                "data/user_continuity.json"
            )
        )

        self.extractor = (
            ContinuityAIExtractor()
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
            ai_client,
            message: str
    ):

        extracted = (
            self.extractor
            .extract_structured_continuity(
                ai_client,
                message
            )
        )

        if (
                extracted["identity"]
                is None
        ):
            return

        memory = (
            self.load_memory()
        )

        existing_item = None

        for item in memory[
            "continuity_items"
        ]:

            if (
                    item["identity"]
                    == extracted["identity"]
            ):
                existing_item = item
                break

        if existing_item:

            existing_item["priority"] += 1

            existing_item["content"] = (
                extracted["content"]
            )

            existing_item["importance"] = (
                extracted["importance"]
            )

        else:

            memory[
                "continuity_items"
            ].append(
                {
                    "identity":
                        extracted["identity"],

                    "type":
                        extracted["type"],

                    "content":
                        extracted["content"],

                    "importance":
                        extracted[
                            "importance"
                        ],

                    "priority": 1
                }
            )

        with open(self.memory_file, "w") as file:
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

        formatted_items = []

        for item in items:
            formatted_items.append(
                (
                    f'- {item["content"]} '
                    f'(importance: '
                    f'{item["importance"]})'
                )
            )

        formatted = "\n".join(
            formatted_items
        )

        return (
            "Known user continuity:\n"
            f"{formatted}"
        )

    def build_priority_briefing(self):

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
        )[:5]

        if not items:
            return ""

        briefing = []

        for item in items:
            briefing.append(
                (
                    f'- {item["identity"]}: '
                    f'{item["content"]}'
                )
            )

        return (
                "Current important continuity areas:\n"
                +
                "\n".join(briefing)
        )