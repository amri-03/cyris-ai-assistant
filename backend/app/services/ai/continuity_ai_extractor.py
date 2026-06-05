import json
import os


class ContinuityAIExtractor:

    def build_extraction_prompt(
            self,
            message: str,
            existing_items_str: str
    ):

        return f"""

        Extract ONLY meaningful long-term continuity information from the user's message.

        You must normalize similar concepts into stable identities.
        
        Do not infer technologies, frameworks, or experiences that the user did not explicitly mention.

        Examples:

        - frontend learning
        - frontend projects
        - frontend internship preparation

        should become:
        "frontend_development"

        - internship preparation
        - internship goals
        - getting internships

        should become:
        "internship_preparation"

        - resume building
        - resume projects

        should become:
        "resume_building"
        
        Do not create new abstract identities unless the user's intent is very clear and repeatedly reinforced.

        Valid continuity types:
        - goal
        - focus_area
        - struggle
        - interest
        - project
        - academic_context
        - career_direction
        
        Extract ONLY information the user personally claims,
        owns, is actively pursuing,
        or clearly identifies with.
        
        Only extract direct user ownership statements such as:
        - "I am learning..."
        - "I want to improve..."
        - "I am working on..."
        - "My project is..."
        - "I struggle with..."
        - "I am in semester..."

        Existing known continuity items for this user:
        {existing_items_str}

        CRITICAL DIRECTIVES:
        1. If the user's statement refers to or updates a topic that already exists in the known items, REUSE the existing "identity" (e.g., if you are updating academic details, reuse the existing identity like "academic_status" or "study_topics" instead of creating a new one).
        2. If the new information completely replaces, updates, or conflicts with one or more existing items, list those old items' identities in the "supersedes" array so they can be retired.
        
        Return ONLY valid JSON.
        
        The information should likely remain relevant across multiple future conversations.
        
        Do NOT extract:
        - hypothetical discussions
        - examples
        - technologies mentioned casually
        - things the user rejected
        - things the user said they don't know
        - assistant suggestions
        - temporary conversational filler
        - speculative interests
        - emotional reactions without long-term significance
        - temporary confusion
        - exploratory thinking
        - hypothetical interests
        - broad career uncertainty without stable direction
        
        If nothing clearly important exists,
        return empty continuity.
        
        Information related to:
        - long-term learning goals
        - career direction
        - recurring struggles
        - academic direction
        - internship preparation
        - stable technical interests
        - repeated productivity challenges
        
        SHOULD usually be extracted.

        Format:
        {{
            "identity": "...",
            "type": "...",
            "content": "...",
            "importance": "low | medium | high",
            "supersedes": ["old_identity_1", "old_identity_2"]
        }}

        If nothing meaningful exists, return:
        {{
            "identity": null
        }}

        User message:
        "{message}"

        """

    def extract_structured_continuity(
            self,
            ai_client,
            message: str,
            existing_items: list = None
    ):
        # Format existing items
        if existing_items:
            items_summary = []
            for item in existing_items:
                items_summary.append({
                    "identity": item.get("identity"),
                    "type": item.get("type"),
                    "content": item.get("content")
                })
            existing_items_str = json.dumps(items_summary, indent=2)
        else:
            existing_items_str = "[]"

        extraction_prompt = (
            self.build_extraction_prompt(
                message,
                existing_items_str
            )
        )

        content = ""
        gemini_key = os.getenv("GEMINI_API_KEY")

        # Try Gemini first as preferred by the user, falling back to Groq if key missing
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(extraction_prompt)
                content = response.text
            except Exception as gemini_err:
                print(f"Gemini extraction failed, falling back to Groq: {gemini_err}")
                gemini_key = None

        if not gemini_key:
            # Fallback to Groq
            if not ai_client:
                from groq import Groq
                groq_key = os.getenv("GROQ_API_KEY")
                ai_client = Groq(api_key=groq_key)
            try:
                response = ai_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": extraction_prompt
                        }
                    ]
                )
                content = response.choices[0].message.content
            except Exception as groq_err:
                print(f"Groq extraction failed: {groq_err}")
                return {"identity": None}

        try:
            cleaned = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            parsed = json.loads(cleaned)

            if not parsed.get("identity"):
                return {
                    "identity": None
                }

            # Ensure supersedes is a list
            if "supersedes" not in parsed or not isinstance(parsed["supersedes"], list):
                parsed["supersedes"] = []

            return parsed

        except Exception:
            return {
                "identity": None
            }