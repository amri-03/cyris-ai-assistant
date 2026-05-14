class AlignmentEngine:

    def evaluate_alignment(
            self,
            long_term_goal: str,
            current_focus: list,
            fragmentation_level: str
    ):

        if (
                fragmentation_level == "high"
                and len(current_focus) > 3
        ):
            return {
                "alignment_status": "drifting",
                "guidance": (
                    "Current focus fragmentation may be reducing "
                    "alignment with long-term direction."
                )
            }

        if long_term_goal not in current_focus:
            return {
                "alignment_status": "misaligned",
                "guidance": (
                    "Current priorities appear disconnected from "
                    "the dominant long-term direction."
                )
            }

        return {
            "alignment_status": "aligned",
            "guidance": (
                "Current focus structure appears reasonably aligned "
                "with long-term direction."
            )
        }