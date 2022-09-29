import re
from typing import Tuple, Union, Match

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.events.utils import split_subject
from battlevideo.event.locale import Locale
from ocr.normalization_ja import normalize
from pokedex.pokedex import Pokedex


class PokemonDownedEvent(Event):

    def __init__(self, message: str, pokemon: str, is_opponent: bool):
        super().__init__(message)
        self.pokemon = pokemon
        self.is_opponent = is_opponent


class PokemonDownedMatcher(EventMatcher):

    def __init__(self, pokedex: Pokedex):
        self.__pokedex = pokedex

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[PokemonDownedEvent, None]]:
        match = re.search("(.+)は\sたおれた!", text)
        if match is not None:
            event = self.__construct_event(match)
            return True, event

        return False, None

    def __construct_event(self, match: Match) -> PokemonDownedEvent:
        pokemon, is_opponent = split_subject(match.group(1))
        pokemon = normalize(pokemon)
        pokemon = self.__pokedex.pokemons_reverse[pokemon]
        message = self.__construct_message(pokemon, is_opponent)
        return PokemonDownedEvent(message, pokemon, is_opponent)

    def __construct_message(self, pokemon: str, is_opponent: bool) -> str:
        return f"{'相手の ' if is_opponent else ''}{pokemon}は たおれた!"
