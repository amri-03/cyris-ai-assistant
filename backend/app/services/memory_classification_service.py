from app.models.classified_memory import ClassifiedMemory


class MemoryClassificationService:

    def classify_memory(
            self,
            identity_traits: list,
            temporary_states: list,
            patterns: list,
            priorities: list
    ):
        memory = ClassifiedMemory()

        memory.persistent_identity.extend(
            identity_traits
        )

        memory.temporary_context.extend(
            temporary_states
        )

        memory.behavioral_patterns.extend(
            patterns
        )

        memory.adaptive_priorities.extend(
            priorities
        )

        return memory