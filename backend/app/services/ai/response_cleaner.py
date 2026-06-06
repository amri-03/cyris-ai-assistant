import re


class ResponseCleaner:

    def clean_thinking_trace(self, text: str) -> str:
        lines = text.splitlines()
        
        # If the text does not contain any bullet points or reasoning markers, return it as is
        if not any(line.strip().startswith('*') for line in lines):
            return text
            
        markers = [
            "drafting the final response:",
            "final result:",
            "response:",
            "*response:",
            "polished selection:",
            "refined selection:"
        ]
        
        for i in range(len(lines) - 1, -1, -1):
            line_lower = lines[i].lower()
            if any(marker in line_lower for marker in markers):
                actual_lines = lines[i+1:]
                result = "\n".join(actual_lines).strip()
                if (result.startswith('"') and result.endswith('"')) or (result.startswith("'") and result.endswith("'")):
                    result = result[1:-1].strip()
                
                sub_lines = result.splitlines()
                if len(sub_lines) >= 2:
                    last_line = sub_lines[-1].strip()
                    second_last_line = sub_lines[-2].strip().strip('"').strip("'")
                    if last_line == second_last_line:
                        return last_line
                return result
                
        # Fallback: find the first line that is not a bullet point/reasoning step
        start_of_response = 0
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('*') or (line.startswith('    ') and (stripped.startswith('-') or stripped.startswith('*'))):
                continue
            if stripped.startswith('(') and stripped.endswith(')'):
                continue
            if any(w in stripped.lower() for w in ["option ", "selection:", "refined selection:", "drafting ", "choice:", "constraint "]):
                continue
            start_of_response = idx
            break
            
        actual_lines = lines[start_of_response:]
        result = "\n".join(actual_lines).strip()
        
        sub_lines = result.splitlines()
        if len(sub_lines) >= 2:
            last_line = sub_lines[-1].strip()
            second_last_line = sub_lines[-2].strip().strip('"').strip("'")
            if last_line == second_last_line:
                return last_line
                
        return result

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