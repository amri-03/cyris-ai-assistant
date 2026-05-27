import json
from pathlib import Path

from app.services.memory.memory_summary_service import (
    MemorySummaryService
)


class ConversationMemoryService:

    def __init__(self):

        self.memory_file = (
            Path(
                "data/conversation_memory.json"
            )
        )

        self.summary_service = (
            MemorySummaryService()
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
                "messages": []
            }

    def save_message(
            self,
            role: str,
            content: str
    ):

        memory = (
            self.load_memory()
        )

        memory["messages"].append(
            {
                "role": role,
                "content": content
            }
        )

        memory["messages"] = (
            memory["messages"][-50:]
        )

        with open(self.memory_file, "w") as file:
            json.dump(
                memory,
                file,
                indent=4
            )

    def build_memory_context(self):

        memory = (
            self.load_memory()
        )

        recent_messages = (
            memory["messages"][-10:]
        )

        summarized_context = (
            self.summary_service
            .build_summary(
                recent_messages
            )
        )

        return summarized_context