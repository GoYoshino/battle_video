from typing import Tuple, Union
import re

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.locale import Locale


class MoveUsedEvent(Event):

    def __init__(self, message: str, pokemon: str, is_opponent: bool, move: str):
        super().__init__(message)
        self.pokemon = pokemon
        self.is_opponent = is_opponent
        self.move = move


class MoveUsedMatcher(EventMatcher):

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[int, None], Union[MoveUsedEvent, None]]:
        match = re.search("(.+)の\n([^\s]+)!$", text)
        if match is not None:
            event = self.__construct_event(match, text)
            return True, 2, event

        match = re.search("(.+)は\n(.+)を\sつかった!$", text)
        if match is not None:
            event = self.__construct_event(match, text)
            return True, 2, event

        return False, None, None

    def __construct_event(self, match: re.Match, message: str) -> MoveUsedEvent:
        pokemon_texts = match.group(1).split(" ")
        if len(pokemon_texts) == 2:
            pokemon = pokemon_texts[1]
            is_opponent = True
        else:
            pokemon = pokemon_texts[0]
            is_opponent = False
        move = match.group(2)

        return MoveUsedEvent(message, pokemon, is_opponent, move)