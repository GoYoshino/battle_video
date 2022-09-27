from typing import List

from battlevideo.battle_state import BattleState
from battlevideo.event.events import Event, PokemonDownedEvent
from battlevideo.event.events.battle_ended import BattleEndedEvent


class BattleVideo:

    def __init__(self, events: List[Event]):
        self.__states: List[BattleState] = []
        self.__annotate(events)

    def __getitem__(self, index: int):
        return self.__states[index]

    def __len__(self):
        return len(self.__states)

    def __repr__(self):
        repr = []
        for state in self.__states:
            repr.append(str(state))
        return "\n".join(repr)

    def __annotate(self, events: List[Event]):
        ally_pokemon_left = 3
        opponent_pokemon_left = 3

        for event in events:
            if isinstance(event, PokemonDownedEvent):
                if event.is_opponent:
                    opponent_pokemon_left -= 1
                else:
                    ally_pokemon_left -= 1
            self.__states.append(BattleState(event, ally_pokemon_left, opponent_pokemon_left))
            if ally_pokemon_left == 0:
                self.__states.append(BattleState(BattleEndedEvent(True), ally_pokemon_left, opponent_pokemon_left))
            elif opponent_pokemon_left == 0:
                self.__states.append(BattleState(BattleEndedEvent(False), ally_pokemon_left, opponent_pokemon_left))
