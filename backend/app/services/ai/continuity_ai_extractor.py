import json


class ContinuityAIExtractor:

    def build_extraction_prompt(
            self,
            message: str
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

        Valid continuity types:
        - goal
        - focus_area
        - struggle
        - interest
        - project

        Return ONLY valid JSON.

        Format:
        {{
            "identity": "...",
            "type": "...",
            "content": "...",
            "importance": "low | medium | high"
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
            message: str
    ):

        extraction_prompt = (
            self.build_extraction_prompt(
                message
            )
        )

        response = (
            ai_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content":
                            extraction_prompt
                    }
                ]
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        try:

            parsed = json.loads(content)

            return parsed

        except Exception:

            return {
                "type": None
            }