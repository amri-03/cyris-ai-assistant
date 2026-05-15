class InteractionAggregator:

    def __init__(self):
        self.total_interactions = 0

    def register_interaction(self):
        self.total_interactions += 1

    def get_total_interactions(self):
        return {
            "total_interactions": (
                self.total_interactions
            )
        }