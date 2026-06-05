import re

class ContinuityExtractor:
    # A broad set of keyword triggers to check if a message has long-term continuity updates.
    # If a message doesn't contain any of these, we skip LLM extraction to save tokens and avoid rate limits.
    CONTINUITY_TOPICS = [
        # Action/Intent & Academics
        "learn", "studies", "academic", "academics", "college", "university", "semester", "sem", "degree", "exam", "exams", "test", "tests", "gpa", "cgpa", "class", "school", "course", "courses", "syllabus", "assignment", "assignments",
        # Career & Goals
        "career", "job", "jobs", "internship", "internships", "placement", "freelance", "freelancing", "resume", "cv", "portfolio", "linkedin", "profile", "goal", "goals", "focus", "target", "targets", "plan", "plans", "schedule", "routine", "routines", "habit", "habits", "todo",
        # Key Technical Focus Areas
        "project", "projects", "coding", "programming", "developer", "development", "frontend", "backend", "fullstack", "design", "ui", "ux", "app", "cybersecurity",
        # Languages & Tools
        "python", "java", "javascript", "js", "typescript", "ts", "rust", "go", "golang", "cpp", "c++", "react", "nextjs", "node", "nodejs", "sql", "database", "databases", "git", "github", "docker", "aws", "cloud", "ai", "ml", "machine learning",
        # Struggles & Behaviors
        "struggle", "struggles", "struggling", "motivate", "motivation", "motivated", "distract", "distraction", "distractions", "consistent", "consistency", "inconsistent", "drift", "drifting", "overwhelm", "overwhelmed", "lazy", "laziness", "procrastinate", "procrastinating", "procrastination", "tired", "burnout", "stress", "stressed", "anxious", "anxiety", "fear", "stuck", "confused", "confusion", "fail", "failed", "failure"
    ]

    def extract_continuity(
            self,
            message: str
    ):
        lowered_message = message.lower()
        matched_topics = []

        for topic in self.CONTINUITY_TOPICS:
            if len(topic) <= 3:
                # Use word boundary check for short words (e.g., 'go', 'ai', 'sem', 'js') to prevent false substrings
                if re.search(rf"\b{re.escape(topic)}\b", lowered_message):
                    matched_topics.append(topic)
            else:
                # Substring match for longer words to capture inflections (e.g., 'procrastinate' matching 'procrastinating')
                if topic in lowered_message:
                    matched_topics.append(topic)

        if not matched_topics:
            return None

        return {
            "content": message,
            "topics": matched_topics
        }