import re


class ResponseCleaner:

    def clean_thinking_trace(self, text: str) -> tuple[str, bool]:
        lines = text.splitlines()
        if not lines:
            return text, False

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
            "state that", "do not get", "do not apologize", "do not explain", "maintain the",
            "potential directions", "options", "refining for", "refining", "refine",
            "consistent with the persona", "simple acknowledgment", "since it's a parting",
            "keep it brief", "final polish"
        ]

        has_thinking = any(indicator in text.lower() for indicator in thinking_indicators)
        has_bullet_structure = any(line.startswith(' ') and '*' in line for line in lines)

        if not (has_thinking or has_bullet_structure):
            return text, False

        # Regex to match planning labels like "Final Polish:", "Refining for persona (Cyris):", "Constraint 1:"
        planning_label_pattern = re.compile(
            r'^(final result|final polish|refining|refine|refinement|persona|role|task|constraint|self-correction|draft|drafting|strategy|approach|selection|context check|check context|option \d+|greeting|acknowledgment|parting)\b',
            re.IGNORECASE
        )

        planning_prefixes = [
            "based on", "therefore", "response strategy", "strategy", "avoid",
            "be accurate", "answer directly", "avoid robotic", "acknowledge",
            "state that", "do not", "maintain the", "self-correction", "drafting",
            "polished selection", "refined selection", "selection:", "final result:",
            "direct approach", "refined approach", "context check", "check context",
            "testing my memory", "check against", "ask clarifying", "persona:",
            "role:", "task:", "constraint", "identity:", "supersedes:",
            "continuity_items:", "importance:", "priority:", "career:", "technical:",
            "academics:", "user context", "user says", "refined (cyris",
            "the user says", "the user", "this is", "the goal", "potential", 
            "options:", "options", "let's go", "let's keep", "let's use", "let's",
            "wait,", "since the", "1. ", "2. ", "3. ", "4. ", "i should", "i will",
            "options and drafting", "drafting response", "here is", "refining for",
            "refining", "keep it brief", "since it's a parting", "simple acknowledgment",
            "consistent with the persona", "final polish"
        ]

        def get_words(t):
            t_clean = re.sub(r'[^\w\s]', '', t.strip().lower())
            return set(t_clean.split())

        response_lines = []
        
        for line in reversed(lines):
            stripped = line.strip()
            if not stripped:
                if response_lines:
                    response_lines.append(line)
                continue
                
            is_indented = line.startswith(' ') or line.startswith('\t')
            
            # Check if the line matches planning label regex or prefixes
            stripped_lower = stripped.lower()
            is_meta_prefix = any(stripped_lower.startswith(pref) for pref in planning_prefixes) or bool(planning_label_pattern.match(stripped_lower))
            
            # Check if the line is bulleted and is planning
            is_bullet_meta = False
            if stripped.startswith('*') or stripped.startswith('-'):
                after_bullet = stripped[1:].strip().lower()
                if any(after_bullet.startswith(pref) for pref in planning_prefixes) or bool(planning_label_pattern.match(after_bullet)):
                    is_bullet_meta = True

            # Check if this line is highly similar to the response collected so far (draft detection)
            is_draft = False
            if response_lines:
                # Combine current response lines to compare
                current_response = " ".join([l for l in response_lines if l.strip()])
                words_response = get_words(current_response)
                words_line = get_words(stripped.strip('"\''))
                
                if words_response and words_line:
                    intersection = words_response.intersection(words_line)
                    overlap_ratio = len(intersection) / min(len(words_response), len(words_line))
                    if overlap_ratio > 0.8:
                        is_draft = True

            if is_indented or is_meta_prefix or is_bullet_meta or is_draft:
                break
                
            response_lines.append(line)
            
        if response_lines:
            response_lines.reverse()
            res = "\n".join(response_lines).strip()
            if (res.startswith('"') and res.endswith('"')) or (res.startswith("'") and res.endswith("'")):
                res = res[1:-1].strip()
            return res, True

        return lines[-1].strip().strip('"'), True

    def clean_response(
            self,
            text: str
    ):
        if not isinstance(text, str):
            return str(text)

        # Remove model internal thoughts/chain-of-thought traces
        cleaned, has_thinking = self.clean_thinking_trace(text)

        # Remove leading timestamps prepended by the model in the form of [YYYY-MM-DD HH:MM] or [YYYY-MM-DD HH:MM:SS]
        cleaned = re.sub(
            r"^\s*\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?\]\s*",
            "",
            cleaned
        )

        if has_thinking:
            # Deduplicate adjacent lines/paragraphs (quoted vs unquoted drafts) if there was thinking trace
            lines = cleaned.splitlines()
            non_empty = [(i, line.strip()) for i, line in enumerate(lines) if line.strip()]
            
            def clean_p(p):
                p_clean = re.sub(r'[^\w\s]', '', p.strip().lower())
                return set(p_clean.split())

            indices_to_remove = set()
            i = 0
            while i < len(non_empty) - 1:
                idx1, l1 = non_empty[i]
                idx2, l2 = non_empty[i+1]
                
                l1_unquoted = l1.strip('"\'')
                l2_unquoted = l2.strip('"\'')
                
                words1 = clean_p(l1_unquoted)
                words2 = clean_p(l2_unquoted)
                
                if words1 and words2:
                    intersection = words1.intersection(words2)
                    union = words1.union(words2)
                    similarity = len(intersection) / len(union) if union else 0
                    
                    if similarity > 0.6 or l1_unquoted == l2_unquoted:
                        # Mark the earlier one for removal
                        indices_to_remove.add(idx1)
                        non_empty.pop(i)
                        continue
                i += 1
            
            reconstructed_lines = []
            for i, line in enumerate(lines):
                if i in indices_to_remove:
                    continue
                reconstructed_lines.append(line)
            cleaned = "\n".join(reconstructed_lines)

        # Deduplicate identical adjacent lines (quoted draft vs unquoted final response)
        lines_list = [line.strip() for line in cleaned.splitlines() if line.strip()]
        if len(lines_list) >= 2:
            l0 = lines_list[-2]
            l1 = lines_list[-1]
            l0_unquoted = l0.strip('"\'')
            l1_unquoted = l1.strip('"\'')
            if l0_unquoted == l1_unquoted:
                all_lines = cleaned.splitlines()
                non_empty_indices = [i for i, line in enumerate(all_lines) if line.strip()]
                if len(non_empty_indices) >= 2:
                    idx_to_remove = non_empty_indices[-2]
                    del all_lines[idx_to_remove]
                    cleaned = "\n".join(all_lines)

        return cleaned.strip()