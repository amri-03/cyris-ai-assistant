class PromptValidation:

    def validate_prompt(
            self,
            prompt
    ):

        if not prompt:
            return {
                "valid": False,

                "prompt_integrity": (
                    "prompt_missing"
                )
            }

        if len(prompt) < 20:
            return {
                "valid": False,

                "prompt_integrity": (
                    "prompt_too_short"
                )
            }

        return {
            "valid": True,

            "prompt_integrity": (
                "prompt_structure_stable"
            )
        }