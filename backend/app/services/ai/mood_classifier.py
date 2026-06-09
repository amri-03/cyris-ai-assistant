import json
import os

class MoodClassifier:
    """
    Lightweight mood classification that runs alongside continuity extraction.
    Analyzes recent conversation context to detect the user's current emotional state.
    """
    VALID_MOODS = [
        "calm", "neutral", "stressed", "frustrated",
        "excited", "motivated", "low_energy", "anxious",
        "overwhelmed", "focused", "confused", "grateful"
    ]

    def build_classification_prompt(self, conversation_context: str):
        valid_moods_str = ", ".join(self.VALID_MOODS)
        return f"""
        Analyze the following conversation and classify the user's current mood.
        Conversation:
        {conversation_context}
        Based on the user's tone, word choice, and emotional signals, classify their current mood as ONE of:
        {valid_moods_str}
        Also assess their energy level as one of: high, medium, low
        Rules:
        - Only classify based on what the user actually expressed, not the assistant's response.
        - If the user's mood is unclear or purely informational, default to "neutral".
        - Do not over-interpret casual conversation as emotional.
        - Keep the context description very brief (under 15 words).
        Return ONLY valid JSON:
        {{
            "mood": "one of the valid moods",
            "energy": "high | medium | low",
            "context": "brief description of what indicates this mood"
        }}
        If the conversation is too short or ambiguous to classify:
        {{
            "mood": "neutral",
            "energy": "medium",
            "context": "insufficient context"
        }}
        """

    def classify_mood(self, ai_client, conversation_context: str):
        """
        Classify the user's current mood from recent conversation context.
        Returns dict with mood, energy, and context fields.
        """
        prompt = self.build_classification_prompt(conversation_context)
        content = ""
        groq_key = os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")

        # Use Groq first (preserves Gemini quota for chat)
        if groq_key:
            try:
                if not ai_client:
                    from groq import Groq
                    ai_client = Groq(api_key=groq_key)
                response = ai_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.choices[0].message.content
            except Exception as e:
                print(f"Groq mood classification failed: {e}")
                groq_key = None

        if not groq_key and gemini_key:
            try:
                import warnings
                warnings.filterwarnings("ignore", category=FutureWarning)
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model_name = os.getenv("GEMINI_MODEL", "gemma-4-26b-a4b-it")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                content = response.text
            except Exception as e:
                print(f"Gemini mood classification failed: {e}")
                return None

        if not content:
            return None

        try:
            start_idx = content.find("{")
            end_idx = content.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx + 1]
            else:
                json_str = content

            cleaned = json_str.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)

            # Validate mood value
            mood = parsed.get("mood", "neutral")
            if mood not in self.VALID_MOODS:
                mood = "neutral"

            energy = parsed.get("energy", "medium")
            if energy not in ["high", "medium", "low"]:
                energy = "medium"

            return {
                "mood": mood,
                "energy": energy,
                "context": parsed.get("context", "")
            }
        except Exception:
            return None
