from unittest import TestCase

from battlevideo.event.events.ally_pokemon_sent import AllyPokemonSentMatcher
from battlevideo.event.locale import Locale

matcher = AllyPokemonSentMatcher()

class AllyPokemonSentMatcherTest(TestCase):

    def test_yuke_matches(self):
        matches, line_consumed, event = matcher.matches("ゆけっ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 1)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_other_message_does_not_match(self):
        matches, line_consumed, event = matcher.matches("ウオノラゴンは\nゴツゴツメットで ダメージを受けた!", Locale.JA)
        self.assertFalse(matches)

    def test_makaseta_matches(self):
        matches, line_consumed, event = matcher.matches("任せた! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 1)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_yowatteiru_matches(self):
        matches, line_consumed, event = matcher.matches("相手が 弱っている!\nチャンスだ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_works_with_titled_pokemon_yuke(self):
        matches, line_consumed, event = matcher.matches("ゆけっ! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 1)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_works_with_titled_pokemon_makaseta(self):
        matches, line_consumed, event = matcher.matches("任せた! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 1)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_works_with_titled_pokemon_yowatteiru(self):
        matches, line_consumed, event = matcher.matches("相手が 弱っている!\nチャンスだ! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("ウオノラゴン", event.pokemon)