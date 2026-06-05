import json
from datetime import datetime
from pathlib import Path

from app.services.ai.continuity_ai_extractor import (
    ContinuityAIExtractor
)
from app.memory.continuity_extractor import ContinuityExtractor


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

        self.rule_extractor = (
            ContinuityExtractor()
        )

    def load_memory(self):
        try:
            # Ensure parent directory exists
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)

            # Auto-create file if missing
            if not self.memory_file.exists():
                default_memory = {"continuity_items": []}
                with open(self.memory_file, "w") as file:
                    json.dump(default_memory, file, indent=4)
                return default_memory

            with open(
                    self.memory_file,
                    "r"
            ) as file:
                return json.load(file)

        except Exception:
            return {
                "continuity_items": []
            }

    def delete_continuity_item(
            self,
            identity: str
    ):
        try:
            memory = self.load_memory()
            memory["continuity_items"] = [
                item for item in memory["continuity_items"]
                if item["identity"] != identity
            ]
            with open(self.memory_file, "w") as file:
                json.dump(
                    memory,
                    file,
                    indent=4
                )
            return True
        except Exception:
            return False

    def save_continuity(
            self,
            ai_client,
            message: str
    ):

        try:
            # Token Efficiency: pre-filter message using rule-based keyword check
            if not self.rule_extractor.extract_continuity(message):
                return

            memory = (
                self.load_memory()
            )
            existing_items = memory.get("continuity_items", [])

            extracted = (
                self.extractor
                .extract_structured_continuity(
                    ai_client,
                    message,
                    existing_items
                )
            )

            if (
                    extracted["identity"]
                    is None
            ):
                return

            # Retiring superseded elements (conflict resolution)
            if extracted.get("supersedes"):
                memory["continuity_items"] = [
                    item for item in memory["continuity_items"]
                    if item["identity"] not in extracted["supersedes"]
                ]

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

            timestamp_str = datetime.now().isoformat()

            if existing_item:

                existing_item["priority"] = min(5, existing_item.get("priority", 3) + 1)

                existing_item["content"] = (
                    extracted["content"]
                )

                existing_item["importance"] = (
                    extracted["importance"]
                )
                
                existing_item["last_updated"] = timestamp_str

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

                        "priority": self.calculate_priority(
                            extracted["type"],
                            extracted["importance"]
                        ),
                        
                        "created_at": timestamp_str,
                        
                        "last_updated": timestamp_str
                    }
                )

            with open(self.memory_file, "w") as file:
                json.dump(
                    memory,
                    file,
                    indent=4
                )

        except Exception:
            return

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

    def calculate_priority(
            self,
            continuity_type,
            importance
    ):

        priority_map = {

            "career_direction": 5,
            "goal": 4,
            "focus_area": 4,
            "project": 4,
            "academic_context": 3,
            "struggle": 5,
            "interest": 2
        }

        importance_bonus = {

            "high": 1,
            "medium": 0,
            "low": -1
        }

        base_priority = (
            priority_map.get(
                continuity_type,
                1
            )
        )

        adjustment = (
            importance_bonus.get(
                importance,
                0
            )
        )

        final_priority = (
                base_priority + adjustment
        )

        return max(
            1,
            min(final_priority, 5)
        )