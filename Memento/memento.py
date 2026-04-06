class RingMemento:
    def __init__(self, state):
        self._state = dict(state)

    def get_state(self):
        return dict(self._state)