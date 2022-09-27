from unittest import TestCase

from battlevideo.event.events.pokemon_downed import PokemonDownedMatcher
from battlevideo.event.locale import Locale

matcher = PokemonDownedMatcher()

class PokemonDownedTest(TestCase):

    def test_does_not_match_at_different_message(self):
        matches, event = matcher.matches("モジャンボの\n攻撃が 上がった!", Locale.JA)
        self.assertFalse(matches)

    def test_ally(self):
        text = "ザシアンは たおれた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ザシアン", event.pokemon)
        self.assertFalse(event.is_opponent)
        self.assertEqual(text, event.message)

    def test_ally_used(self):
        text = "相手の ザシアンは たおれた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ザシアン", event.pokemon)
        self.assertTrue(event.is_opponent)
        self.assertEqual(text, event.message)
