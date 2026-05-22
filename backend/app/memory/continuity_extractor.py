class ContinuityExtractor:
    CONTINUITY_TOPICS = [
        "frontend",
        "backend",
        "resume",
        "internship",
        "career",
        "project",
        "projects",
        "study",
        "studies",
        "academic",
        "academics",
        "sem",
        "semester",
        "design",
        "designing",
        "cybersecurity",
        "learning",
        "improve",
        "improving",
        "skills",
        "focus",
        "goal",
        "freelancing"
    ]

    def extract_continuity(
            self,
            message: str
    ):

        lowered_message = (
            message.lower()
        )

        matched_topics = []

        for topic in (
                self.CONTINUITY_TOPICS
        ):

            if topic in lowered_message:
                matched_topics.append(
                    topic
                )

        if not matched_topics:
            return None

        return {
            "content": message,
            "topics": matched_topics
        }