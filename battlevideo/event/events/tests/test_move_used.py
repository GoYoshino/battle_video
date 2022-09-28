from unittest import TestCase

from battlevideo.event.events.move_used import MoveUsedMatcher
from battlevideo.event.locale import Locale
from pokedex.pokedex import Pokedex

pokedex = Pokedex()
matcher = MoveUsedMatcher(pokedex)

class MoveUsedTest(TestCase):

    def test_does_not_match_at_different_message(self):
        matches, event = matcher.matches("モジャンボは たおれた!", Locale.JA)
        self.assertFalse(matches)

    def test_does_not_match_at_same_structure(self):
        matches, event = matcher.matches("モジャンボの\n攻撃が 上がった!", Locale.JA)
        self.assertFalse(matches)

    def test_ally_standard(self):
        text = "モジャンボの\nリーフストーム!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertFalse(event.is_opponent)
        self.assertTrue("リーフストーム", event.move)

    def test_opponent_standard(self):
        text = "相手の モジャンボの\nリーフストーム!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertTrue(event.is_opponent)
        self.assertTrue("リーフストーム", event.move)

    def test_ally_used(self):
        text = "モジャンボは\nはたきおとすを つかった!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertFalse(event.is_opponent)
        self.assertTrue("はたきおとす", event.move)

    def test_opponent_used(self):
        text = "相手の モジャンボは\nはたきおとすを つかった!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertTrue(event.is_opponent)
        self.assertTrue("はたきおとす", event.move)

    def test_does_normalized_match_for_small_chars(self):
        text = "相手の モジャンボは\nはたきおとすを つかつた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)

    def test_normalized_text_are_revised_for_small_chars(self):
        text = "相手の モジャンボは\nはたきおとすを つかつた!"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("相手の モジャンボは\nはたきおとすを つかった!", event.message)

    def test_type1_tolerates_lost_exclamation_mark(self):
        text = "相手の モジャンボの\nリーフストーム"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)

    def test_type1_revised_for_lost_exclamation_mark(self):
        text = "相手の モジャンボの\nリーフストーム"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("相手の モジャンボの\nリーフストーム!", event.message)

    def test_type2_tolerates_lost_exclamation_mark(self):
        text = "相手の モジャンボは\nはたきおとすを つかった"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)

    def test_type2_revised_for_lost_exclamation_mark(self):
        text = "相手の モジャンボは\nはたきおとすを つかった"
        matches, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("相手の モジャンボは\nはたきおとすを つかった!", event.message)
