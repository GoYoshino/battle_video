from typing import List, Union

from pokedex.pokedex import Pokedex
from .locale import Locale
from .events import Event, EventMatcher, AllyPokemonSentMatcher, OpponentPokemonSentMatcher, MoveUsedMatcher, PokemonDownedMatcher

def text_to_event(text: str, pokedex: Pokedex) -> Union[Event, None]:
    matchers: List[EventMatcher] = [
        AllyPokemonSentMatcher(),
        OpponentPokemonSentMatcher(),
        MoveUsedMatcher(pokedex),
        PokemonDownedMatcher()
    ]

    for matcher in matchers:
        matches, event = matcher.matches(text, Locale.JA, pokedex)
        if matches:
            return event

    return None
