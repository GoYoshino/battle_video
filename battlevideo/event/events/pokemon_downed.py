import re
from typing import Tuple, Union

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.locale import Locale


class PokemonDownedEvent(Event):

    def __init__(self, message: str, pokemon: str, is_opponent: bool):
        super().__init__(message)
        self.pokemon = pokemon
        self.is_opponent = is_opponent


class PokemonDownedMatcher(EventMatcher):

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[int, None], Union[PokemonDownedEvent, None]]:
        match = re.search("(.+)は\sたおれた!", text)
        if match is not None:
            event = self.__construct_event(match, text)
            return True, 1, event

        return False, None, None

    def __construct_event(self, match: re.Match, message: str) -> PokemonDownedEvent:
        pokemon_texts = match.group(1).split(" ")
        if len(pokemon_texts) == 2:
            pokemon = pokemon_texts[1]
            is_opponent = True
        else:
            pokemon = pokemon_texts[0]
            is_opponent = False

        return PokemonDownedEvent(message, pokemon, is_opponent)
