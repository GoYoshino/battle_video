from typing import Tuple, List, Union
import re

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.locale import Locale


class OpponentPokemonSentEvent(Event):

    def __init__(self, message: str, pokemon: str):
        super().__init__(message)
        self.pokemon = pokemon


class OpponentPokemonSentMatcher(EventMatcher):

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[int, None], Union[OpponentPokemonSentEvent, None]]:
        match = re.search(".+は\n(.+)を くりだした!$", text)
        if match is not None:
            pokemon = self.__get_pokemon_name(match.group(1))
            return True, 2, OpponentPokemonSentEvent(text, pokemon)

        return False, None, None

    def __get_pokemon_name(self, string: str):
        parts = string.split(" ")
        return parts[len(parts) - 1]