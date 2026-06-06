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
        - user_preference
        
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
        - "Remember that I..."
        - "Store in memory..."
        - "Keep in mind..."

        Existing known continuity items for this user:
        {existing_items_str}

        CRITICAL DIRECTIVES:
        1. If the user's statement refers to or updates a topic that already exists in the known items, REUSE the existing "identity" (e.g., if you are updating academic details, reuse the existing identity like "academic_status" or "study_topics" instead of creating a new one).
        2. If the new information completely replaces, updates, or conflicts with one or more existing items, list those old items' identities in the "supersedes" array so they can be retired.
        3. If the user explicitly asks you to remember or store something (e.g., "remember my favorite color is blue" or "keep in mind that I prefer..."), you MUST extract this fact. Map it to the closest category (like "user_preference" or "interest") and capture the core detail exactly as requested.
        
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
            "continuity_items": [
                {{
                    "identity": "...",
                    "type": "...",
                    "content": "...",
                    "importance": "low | medium | high",
                    "supersedes": ["old_identity_1", "old_identity_2"]
                }}
            ]
        }}

        If nothing meaningful exists, return:
        {{
            "continuity_items": []
        }}

        Recent Conversation Context:
        {message}
        
        Analyze the conversation above, focusing on the user's latest statement and its context, and extract any new or updated long-term continuity details.
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
        groq_key = os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")

        # Try Groq first for extraction to preserve the limited Gemini daily quota (20 RPD) for chat
        if groq_key:
            try:
                if not ai_client:
                    from groq import Groq
                    ai_client = Groq(api_key=groq_key)
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
                print(f"Groq extraction failed, falling back to Gemini: {groq_err}")
                groq_key = None

        if not groq_key and gemini_key:
            try:
                import warnings
                warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model_name = os.getenv("GEMINI_MODEL", "gemma-4-26b-a4b-it")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(extraction_prompt)
                content = response.text
            except Exception as gemini_err:
                print(f"Gemini extraction failed: {gemini_err}")
                return {"continuity_items": []}

        if not content:
            return {"continuity_items": []}

        try:
            # Robust extraction: isolate JSON block by finding the first '{' and last '}'
            start_idx = content.find("{")
            end_idx = content.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx + 1]
            else:
                json_str = content

            cleaned = (
                json_str
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            parsed = json.loads(cleaned)

            if "continuity_items" not in parsed:
                # Normalize old single-item format to list
                if parsed.get("identity"):
                    return {"continuity_items": [parsed]}
                return {"continuity_items": []}

            # Ensure all items have a valid supersedes list
            for item in parsed["continuity_items"]:
                if "supersedes" not in item or not isinstance(item["supersedes"], list):
                    item["supersedes"] = []

            return parsed

        except Exception:
            return {
                "continuity_items": []
            }