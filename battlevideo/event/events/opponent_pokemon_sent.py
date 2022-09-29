from typing import Tuple, List, Union, Match
import re

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.events.utils import remove_title
from battlevideo.event.locale import Locale
from ocr.normalization_ja import normalize
from pokedex.pokedex import Pokedex


class OpponentPokemonSentEvent(Event):

    def __init__(self, message: str, pokemon: str, meta_opponent_name: str):
        super().__init__(message)
        self.pokemon = pokemon
        self.meta_opponent_name = meta_opponent_name


class OpponentPokemonSentMatcher(EventMatcher):

    def __init__(self, pokedex: Pokedex):
        self.__pokedex = pokedex

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[OpponentPokemonSentEvent, None]]:
        match = re.search("(.+)は\n(.+)を くりだした!$", text)
        if match is not None:
            return True, self.__construct_event(match)

        return False, None

    def __construct_event(self, match: Match) -> OpponentPokemonSentEvent:
        opponent_name = match.group(1)
        pokemon_normalized = normalize(remove_title(match.group(2)))
        pokemon = self.__pokedex.pokemons_reverse[pokemon_normalized]
        message = self.__construct_message(pokemon, opponent_name)
        return OpponentPokemonSentEvent(message, pokemon, opponent_name)

    def __construct_message(self, pokemon: str, opponent_name: str):
        return f"{opponent_name}は\n{pokemon}を くりだした!"
