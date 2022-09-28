from enum import Enum
from typing import Tuple, Union
import re

from typing.re import Match

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.events.normalized_match import normalized_search
from battlevideo.event.events.utils import split_subject
from battlevideo.event.locale import Locale
from pokedex.pokedex import Pokedex


class MoveUsedMessageType(Enum):
    STRAIGHT = 0
    USED = 1


class MoveUsedEvent(Event):
    def __init__(self, message: str, pokemon: str, is_opponent: bool, move: str):
        super().__init__(message)
        self.pokemon = pokemon
        self.is_opponent = is_opponent
        self.move = move


class MoveUsedMatcher(EventMatcher):
    def __init__(self, pokedex: Pokedex):
        self.__pokedex = pokedex

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[MoveUsedEvent, None]]:
        match = normalized_search("(.+)の\n([^\s^!]+)[!]?$", text)
        if match is not None:
            event = self.__construct_event(match, MoveUsedMessageType.STRAIGHT)
            return True, event

        match = normalized_search("(.+)は\n(.+)を\sつかった[!]?$", text)
        if match is not None:
            event = self.__construct_event(match, MoveUsedMessageType.USED)
            return True, event

        return False, None

    def __construct_event(self, match: Match, message_type: MoveUsedMessageType) -> MoveUsedEvent:
        pokemon, is_opponent = split_subject(match.group(1))
        pokemon = self.__pokedex.pokemons_reverse[pokemon]
        move = match.group(2)
        message = self.__construct_message(message_type, is_opponent, pokemon, move)

        return MoveUsedEvent(message, pokemon, is_opponent, move)

    def __construct_message(self, message_type: MoveUsedMessageType, is_opponent: bool, pokemon: str, move: str) -> str:
        subject = "相手の " + pokemon if is_opponent else pokemon
        if message_type == MoveUsedMessageType.STRAIGHT:
            return f"{subject}の\n{move}!"
        elif message_type == MoveUsedMessageType.USED:
            return f"{subject}は\n{move}を つかった!"
        raise NotImplementedError()
