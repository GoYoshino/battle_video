from battlevideo.battle_state import BattleState
from battlevideo.event.events import Event


class Memento:
    def __init__(self, event: Event, state: BattleState):
        self.event = event
        self.state = state

    def __repr__(self):
        return self.event.__repr__()
