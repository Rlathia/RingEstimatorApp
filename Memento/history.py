from Memento.memento import RingMemento

class History:
    def __init__(self):
        self._states = []

    def get_history(self):
        return self._states    

    def save(self, memento):
        self._states.append(memento)
