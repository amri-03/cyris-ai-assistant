import re


class ResponseCleaner:

    def clean_thinking_trace(self, text: str) -> str:
        lines = text.splitlines()
        if not lines:
            return text

        # Global indicators (if none of these are in the text, it has no thinking trace at all)
        thinking_indicators = [
            "user context", "user says", "persona:", "self-correction", "final result",
            "drafting", "polished selection", "refined selection", "option 1", "option 2",
            "option 3", "constraint 1", "constraint 2", "constraint 3", "do not invent",
            "do not assume", "ask clarifying", "testing my memory", "check against",
            "direct approach", "refined approach", "context check:", "check context",
            "refined (cyris", "selection:", "role:", "task:", "constraint:", "thinking trace", 
            "chain of thought", "reasoning:", "academic_status", "career_direction",
            "java_learning", "project_development", "the user is asking", "user is asking",
            "previous response", "current continuity", "memory contains", "does the memory",
            "don't know", "acknowledge", "be honest", "user context:", "identity:",
            "supersedes:", "continuity_items", "importance:", "priority:",
            "career:", "technical:", "academics:",
            "based on this context", "therefore", "response strategy", "strategy:",
            "avoid ", "be accurate", "answer directly", "avoid robotic", "acknowledge ",
            "state that", "do not get", "do not apologize", "do not explain", "maintain the"
        ]

        has_thinking = any(indicator in text.lower() for indicator in thinking_indicators)
        # Fallback to general bullet check just in case, but keep it narrow to avoid false positives
        has_bullet_structure = any(line.startswith(' ') and '*' in line for line in lines)

        if not (has_thinking or has_bullet_structure):
            return text

        # Prefixes that indicate a line is a thinking/planning line
        planning_prefixes = [
            "based on", "therefore", "response strategy", "strategy", "avoid",
            "be accurate", "answer directly", "avoid robotic", "acknowledge",
            "state that", "do not", "maintain the", "self-correction", "drafting",
            "polished selection", "refined selection", "selection:", "final result:",
            "direct approach", "refined approach", "context check", "check context",
            "testing my memory", "check against", "ask clarifying", "persona:",
            "role:", "task:", "constraint", "identity:", "supersedes:",
            "continuity_items:", "importance:", "priority:", "career:", "technical:",
            "academics:", "user context", "user says", "refined (cyris"
        ]

        response_lines = []
        
        for line in reversed(lines):
            stripped = line.strip()
            if not stripped:
                if response_lines:
                    response_lines.append(line)
                continue
                
            is_indented = line.startswith(' ') or line.startswith('\t')
            
            # Check if the line starts with any planning prefix
            stripped_lower = stripped.lower()
            is_meta_prefix = any(stripped_lower.startswith(pref) for pref in planning_prefixes)
            
            # Check if the line is bulleted and the text after bullet starts with planning prefix
            is_bullet_meta = False
            if stripped.startswith('*') or stripped.startswith('-'):
                after_bullet = stripped[1:].strip().lower()
                if any(after_bullet.startswith(pref) for pref in planning_prefixes):
                    is_bullet_meta = True

            if is_indented or is_meta_prefix or is_bullet_meta:
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