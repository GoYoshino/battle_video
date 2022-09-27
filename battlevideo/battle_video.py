from typing import List

from battlevideo.event.events import Event


class BattleVideo:

    def __init__(self, events: List[Event]):
        self. __events = events

    def __getitem__(self, index: int):
        return self.__events[index]

    def __len__(self):
        return len(self.__events)

    def __repr__(self):
        repr = []
        for event in self.__events:
            repr.append(event.message)
        return "\n".join(repr)
