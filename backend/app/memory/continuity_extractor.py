class ContinuityExtractor:
    # A broad set of keyword triggers to check if a message has long-term continuity updates.
    # If a message doesn't contain any of these, we skip LLM extraction.
    CONTINUITY_TOPICS = [
        # Academics
        "study", "studies", "academic", "academics", "sem", "semester", "college", "university", "degree", "class", "school",
        # Career & Goals
        "career", "job", "jobs", "internship", "internships", "placement", "mnc", "freelance", "freelancing", "resume", "cv", "portfolio", "linkedin", "profile", "goal", "goals", "focus",
        # Key Technical Focus Areas
        "frontend", "backend", "cybersecurity", "design", "designing", "python", "programming", "coding", "web development",
        # Struggles & Behaviors
        "struggle", "struggles", "motivate", "motivation", "motivated", "distract", "distraction", "distractions", "consistent", "consistency", "inconsistent", "drift", "drifting", "overwhelm"
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