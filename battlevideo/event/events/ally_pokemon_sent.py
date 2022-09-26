from typing import Tuple, List, Union
import re

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.locale import Locale


class AllyPokemonSentEvent(Event):

    def __init__(self, message: str, pokemon: str):
        super().__init__(message)
        self.pokemon = pokemon


class AllyPokemonSentMatcher(EventMatcher):

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[int, None], Union[AllyPokemonSentEvent, None]]:
        match = re.search("ゆけっ!\s(.+)!$", text)
        if match is not None:
            pokemon = self.__get_pokemon_name(match.group(1))
            return True, 1, AllyPokemonSentEvent(text, pokemon)

        match = re.search("相手が\s弱っている!\nチャンスだ!\s(.+)!$", text)
        if match is not None:
            pokemon = self.__get_pokemon_name(match.group(1))
            return True, 2, AllyPokemonSentEvent(text, pokemon)

        match = re.search("任せた!\s(.+)!$", text)
        if match is not None:
            pokemon = self.__get_pokemon_name(match.group(1))
            return True, 1, AllyPokemonSentEvent(text, pokemon)

        return False, None, None

    def __get_pokemon_name(self, string: str):
        parts = string.split(" ")
        return parts[len(parts) - 1]