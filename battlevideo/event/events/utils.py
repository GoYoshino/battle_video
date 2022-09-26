from typing import Tuple


def split_subject(text: str) -> Tuple[str, bool]:
    pokemon_texts = text.split(" ")
    if len(pokemon_texts) == 2:
        pokemon = pokemon_texts[1]
        is_opponent = True
    else:
        pokemon = pokemon_texts[0]
        is_opponent = False
    return pokemon, is_opponent