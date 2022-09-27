from unittest import TestCase

from battlevideo import BattleVideo
from battlevideo.event.events import PokemonDownedEvent, AllyPokemonSentEvent
from battlevideo.event.events.battle_ended import BattleEndedEvent


class BattleVideoTest(TestCase):

    def test_counts_opponent_pokemon(self):
        video = BattleVideo([
            AllyPokemonSentEvent("", "ミミッキュ"),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
        ])
        self.assertEqual(3, video[0].state.opponent_pokemons_left)
        self.assertEqual(2, video[1].state.opponent_pokemons_left)
        self.assertEqual(1, video[2].state.opponent_pokemons_left)
        self.assertEqual(0, video[3].state.opponent_pokemons_left)

    def test_counts_ally_pokemon(self):
        video = BattleVideo([
            AllyPokemonSentEvent("", "ミミッキュ"),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
        ])
        self.assertEqual(3, video[0].state.ally_pokemons_left)
        self.assertEqual(2, video[1].state.ally_pokemons_left)
        self.assertEqual(1, video[2].state.ally_pokemons_left)
        self.assertEqual(0, video[3].state.ally_pokemons_left)

    def test_inserts_win_when_opponent_is_zero(self):
        video = BattleVideo([
            AllyPokemonSentEvent("", "ミミッキュ"),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=True),
        ])
        self.assertIsInstance(video[4].event, BattleEndedEvent)
        self.assertFalse(video[4].event.winner_is_opponent)

    def test_inserts_lose_when_ally_is_zero(self):
        video = BattleVideo([
            AllyPokemonSentEvent("", "ミミッキュ"),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
            PokemonDownedEvent("", "ミミッキュ", is_opponent=False),
        ])
        self.assertIsInstance(video[4].event, BattleEndedEvent)
        self.assertTrue(video[4].event.winner_is_opponent)
