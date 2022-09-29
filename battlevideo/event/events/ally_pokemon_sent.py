from enum import Enum
from typing import Tuple, List, Union, Match

from battlevideo.event.events.event import Event
from battlevideo.event.events.event_matcher import EventMatcher
from battlevideo.event.events.normalized_match import normalized_search
from battlevideo.event.locale import Locale
from pokedex.pokedex import Pokedex


class AllyPokemonSentEvent(Event):

    def __init__(self, message: str, pokemon: str):
        super().__init__(message)
        self.pokemon = pokemon


class AllyPokemonSentMessageType(Enum):
    GO = 1
    IM_COUNTING_ON_YOU = 2
    TAKE_YOUR_CHANCE = 3

class AllyPokemonSentMatcher(EventMatcher):

    def __init__(self, pokedex: Pokedex):
        self.__pokedex = pokedex

    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[AllyPokemonSentEvent, None]]:
        match = normalized_search("ゆけつ!\s(.+)!$", text)
        if match is not None:
            event = self.__construct_event(match, AllyPokemonSentMessageType.GO)
            return True, event

        match = normalized_search("任せた!\s(.+)!$", text)
        if match is not None:
            event = self.__construct_event(match, AllyPokemonSentMessageType.IM_COUNTING_ON_YOU)
            return True, event

        match = normalized_search("相手が\s弱つている!\nチヤンスだ!\s(.+)!$", text)
        if match is not None:
            event = self.__construct_event(match, AllyPokemonSentMessageType.TAKE_YOUR_CHANCE)
            return True, event

        return False, None

    def __get_pokemon_name(self, string: str):
        parts = string.split(" ")
        return parts[len(parts) - 1]

    def __construct_event(self, match: Match, message_type: AllyPokemonSentMessageType) -> AllyPokemonSentEvent:
        pokemon = remove_title(match.group(1))
        pokemon = self.__pokedex.pokemons_reverse[pokemon]
        # TODO: 逆引き辞書にヒットしなかったパターンの処理を考える
        message = self.__construct_message(message_type, pokemon)

        return AllyPokemonSentEvent(message, pokemon)

    def __construct_message(self, message_type: AllyPokemonSentMessageType, pokemon: str) -> str:
        if message_type == AllyPokemonSentMessageType.GO:
            return f"ゆけっ! {pokemon}!"
        elif message_type == AllyPokemonSentMessageType.IM_COUNTING_ON_YOU:
            return f"任せた! {pokemon}!"
        elif message_type == AllyPokemonSentMessageType.TAKE_YOUR_CHANCE:
            return f"相手が 弱っている!\nチャンスだ! {pokemon}!"
        raise NotImplementedError()

def remove_title(pokemon_text: str) -> str:
    if " " not in pokemon_text:
        return pokemon_text

    # 称号は捨てる　かなしいね・・
    return pokemon_text.split(" ")[1]
