import re


class ResponseCleaner:

    def clean_response(
            self,
            text: str
    ):
        if not isinstance(text, str):
            return str(text)

        cleaned = text

        # Remove bold markdown
        cleaned = re.sub(
            r"\*\*(.*?)\*\*",
            r"\1",
            cleaned
        )

        # Remove italic markdown
        cleaned = re.sub(
            r"\*(.*?)\*",
            r"\1",
            cleaned
        )

        # Remove markdown headers
        cleaned = re.sub(
            r"^#+\s",
            "",
            cleaned,
            flags=re.MULTILINE
        )

        # Remove bullet prefixes
        cleaned = re.sub(
            r"^\s*[-•]\s+",
            "",
            cleaned,
            flags=re.MULTILINE
        )

        return cleaned.strip()