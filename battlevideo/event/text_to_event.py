from typing import List, Union

from .locale import Locale
from .events import Event, EventMatcher, AllyPokemonSentMatcher, OpponentPokemonSentMatcher, MoveUsedMatcher, PokemonDownedMatcher

matchers: List[EventMatcher] = [
    AllyPokemonSentMatcher(),
    OpponentPokemonSentMatcher(),
    MoveUsedMatcher(),
    PokemonDownedMatcher()
]

def text_to_event(text: str) -> Union[Event, None]:
    for matcher in matchers:
        matches, event = matcher.matches(text, Locale.JA)
        if matches:
            return event

    return None
