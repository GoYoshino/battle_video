from unittest import TestCase

from battlevideo.event.events.opponent_pokemon_sent import OpponentPokemonSentMatcher
from battlevideo.event.locale import Locale

matcher = OpponentPokemonSentMatcher()

class OpponentPokemonSentMatcherTest(TestCase):

    def test_matches(self):
        matches, line_consumed, event = matcher.matches("グリーンは\nザシアンを くりだした!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("ザシアン", event.pokemon)

    def test_other_message_does_not_match(self):
        matches, line_consumed, event = matcher.matches("ウオノラゴンは\nゴツゴツメットで ダメージを受けた!", Locale.JA)
        self.assertFalse(matches)

    def test_works_with_titled_pokemon(self):
        matches, line_consumed, event = matcher.matches("グリーンは\nランクマスター ザシアンを くりだした!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("ザシアン", event.pokemon)
