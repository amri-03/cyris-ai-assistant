class ContinuityExtractor:
    KEYWORDS = [
        "working",
        "project",
        "goal",
        "improve",
        "learning",
        "studying",
        "focus",
        "resume",
        "internship",
        "frontend",
        "backend",
        "career",
        "problem",
        "struggling"
    ]

    def extract_continuity(
            self,
            message: str
    ):

        lowered_message = (
            message.lower()
        )

        for keyword in self.KEYWORDS:

            if keyword in lowered_message:
                return message

        return None