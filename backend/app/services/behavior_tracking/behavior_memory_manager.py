class BehaviorMemoryManager:

    def __init__(self):
        self.behavior_history = []

    def store_behavior_signal(
            self,
            signal
    ):
        self.behavior_history.append(
            signal
        )

    def get_behavior_history(self):
        return self.behavior_history