import re


class ResponseCleaner:

    def clean_thinking_trace(self, text: str) -> str:
        lines = text.splitlines()
        if not lines:
            return text

        thinking_indicators = [
            "user context", "user says", "persona:", "self-correction", "final result",
            "drafting ", "polished selection", "refined selection", "option 1", "option 2",
            "option 3", "constraint 1", "constraint 2", "constraint 3", "do not invent",
            "do not assume", "ask clarifying", "testing my memory", "check against",
            "direct approach", "refined approach", "context check:", "check context",
            "refined (cyris", "selection:", "role:", "task:", "constraint:", "thinking trace", 
            "chain of thought", "reasoning:"
        ]

        has_thinking = any(indicator in text.lower() for indicator in thinking_indicators)
        # Fallback to general bullet check just in case, but keep it narrow to avoid false positives
        has_bullet_structure = any(line.startswith(' ') and '*' in line for line in lines)

        if not (has_thinking or has_bullet_structure):
            return text

        response_lines = []
        
        for line in reversed(lines):
            stripped = line.strip()
            if not stripped:
                if response_lines:
                    response_lines.append(line)
                continue
                
            is_indented = line.startswith(' ') or line.startswith('\t')
            is_meta = False
            line_lower = stripped.lower()
            if any(kw in line_lower for kw in thinking_indicators):
                is_meta = True

            # We break if the line is indented (as Gemma/Llama's thinking traces are indented)
            # or if the line contains explicit meta/planning keywords.
            if is_indented or is_meta:
                break
                
            response_lines.append(line)
            
        if response_lines:
            response_lines.reverse()
            res = "\n".join(response_lines).strip()
            if (res.startswith('"') and res.endswith('"')) or (res.startswith("'") and res.endswith("'")):
                res = res[1:-1].strip()
            return res

        return lines[-1].strip().strip('"')

    def clean_response(
            self,
            text: str
    ):
        if not isinstance(text, str):
            return str(text)

        # Remove model internal thoughts/chain-of-thought traces
        cleaned = self.clean_thinking_trace(text)

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