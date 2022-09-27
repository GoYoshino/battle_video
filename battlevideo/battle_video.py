from typing import List

from battlevideo.battle_state import BattleState
from battlevideo.event.events import Event, PokemonDownedEvent
from battlevideo.event.events.battle_ended import BattleEndedEvent
from battlevideo.memento import Memento


class BattleVideo:

    def __init__(self, events: List[Event]):
        self.__mementos: List[Memento] = []
        self.__annotate(events)

    def __getitem__(self, index: int) -> Memento:
        return self.__mementos[index]

    def __len__(self) -> int:
        return len(self.__mementos)

    def __repr__(self):
        repr = []
        for memento in self.__mementos:
            repr.append(str(memento))
        return "\n".join(repr)

    def __annotate(self, events: List[Event]) -> None:
        ally_pokemon_left = 3
        opponent_pokemon_left = 3

        for event in events:
            if isinstance(event, PokemonDownedEvent):
                if event.is_opponent:
                    opponent_pokemon_left -= 1
                else:
                    ally_pokemon_left -= 1
            state = BattleState(ally_pokemon_left, opponent_pokemon_left)
            self.__mementos.append(Memento(event, state))
            if ally_pokemon_left == 0:
                self.__mementos.append(Memento(BattleEndedEvent(True), state))
            elif opponent_pokemon_left == 0:
                self.__mementos.append(Memento(BattleEndedEvent(False), state))

