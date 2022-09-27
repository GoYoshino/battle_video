from typing import List

from battlevideo.event.events import Event


class BattleVideo:

    def __init__(self, events: List[Event]):
        self. __events = events

    def __getitem__(self, index: int):
        return self.__events[index]

    def __len__(self):
        return len(self.__events)
