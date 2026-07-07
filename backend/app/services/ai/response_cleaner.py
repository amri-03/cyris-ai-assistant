import re


class ResponseCleaner:

    def clean_thinking_trace(self, text: str) -> tuple[str, bool]:
        """
        Strips internal reasoning wrapped in <thinking>...</thinking> tags.
        Handles unclosed tags gracefully.
        """
        if not isinstance(text, str):
            return str(text), False

        cleaned = re.sub(r'<thinking>.*?(?:</thinking>|$)', '', text, flags=re.DOTALL)
        has_thinking = len(cleaned) < len(text)
        return cleaned.strip(), has_thinking

    def clean_response(self, text: str) -> str:
        if not isinstance(text, str):
            return str(text)

        # Remove model internal thoughts/chain-of-thought traces
        cleaned, _ = self.clean_thinking_trace(text)

        # Remove leading timestamps prepended by the model in the form of [YYYY-MM-DD HH:MM] or [YYYY-MM-DD HH:MM:SS]
        cleaned = re.sub(
            r"^\s*\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?\]\s*",
            "",
            cleaned
        )

        return cleaned.strip()