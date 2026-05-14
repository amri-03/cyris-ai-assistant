class PatternAnalysisService:

    def analyze_patterns(
            self,
            inactivity_events: int,
            overload_events: int,
            focus_switches: int
    ):

        patterns = []

        if inactivity_events >= 3:
            patterns.append(
                "Recurring disengagement pattern detected."
            )

        if overload_events >= 2:
            patterns.append(
                "Repeated overload periods detected."
            )

        if focus_switches >= 4:
            patterns.append(
                "Frequent focus switching detected."
            )

        if not patterns:
            patterns.append(
                "Behavioral patterns currently appear stable."
            )

        return {
            "detected_patterns": patterns
        }