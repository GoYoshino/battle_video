from typing import List, Union

from pokedex.pokedex import Pokedex
from .battle_video import BattleVideo
from battlevideo.event import text_to_event


def parse_texts_to_battle_video(texts: List[str], pokedex: Pokedex) -> BattleVideo:

    previous_text = ""
    events = []

    for text in texts:
        event = text_to_event(text, pokedex)
        if event is not None:
            if text != previous_text:
                events.append(event)

        previous_text = text

    return BattleVideo(events)
