class RingMemento:
    def __init__(self, state):
        self._state = state.copy()

    def get_state(self):
        return self._state.copy()