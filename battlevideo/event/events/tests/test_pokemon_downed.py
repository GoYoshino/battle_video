from unittest import TestCase

from battlevideo.event.events.pokemon_downed import PokemonDownedMatcher
from battlevideo.event.locale import Locale
from pokedex.pokedex import Pokedex

matcher = PokemonDownedMatcher(Pokedex())

class PokemonDownedTest(TestCase):

    def test_does_not_match_at_different_message(self):
        matches, event = matcher.matches("モジャンボの\n攻撃が 上がった!", Locale.JA)
        self.assertFalse(matches)

    def test_works_on_ally(self):
        text = "ザシアンは たおれた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ザシアン", event.pokemon)
        self.assertFalse(event.is_opponent)
        self.assertEqual(text, event.message)

    def test_works_on_opponent(self):
        text = "相手の ザシアンは たおれた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ザシアン", event.pokemon)
        self.assertTrue(event.is_opponent)
        self.assertEqual(text, event.message)

    def test_revises_pokemon_name(self):
        text = "ウソツキーは たおれた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウソッキー", event.pokemon)
        self.assertFalse(event.is_opponent)
        self.assertEqual("ウソッキーは たおれた!", event.message)
