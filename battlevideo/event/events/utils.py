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


def remove_title(pokemon_text: str) -> str:
    if " " not in pokemon_text:
        return pokemon_text

    # 称号は捨てる　かなしいね・・
    return pokemon_text.split(" ")[1]

