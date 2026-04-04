class History:
    def __init__(self):
        self._states = []

    def save(self, state):
        self._states.append(state)
