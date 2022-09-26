from unittest import TestCase

from battlevideo.event.events.move_used import MoveUsedMatcher
from battlevideo.event.locale import Locale

matcher = MoveUsedMatcher()

class MoveUsedTest(TestCase):

    def test_does_not_match_at_different_message(self):
        matches, line_consumed, event = matcher.matches("モジャンボは たおれた!", Locale.JA)
        self.assertFalse(matches)

    def test_does_not_match_at_same_structure(self):
        matches, line_consumed, event = matcher.matches("モジャンボの\n攻撃が 上がった!", Locale.JA)
        self.assertFalse(matches)

    def test_ally_standard(self):
        text = "モジャンボの\nリーフストーム!"
        matches, line_consumed, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertFalse(event.is_opponent)
        self.assertTrue("リーフストーム", event.move)

    def test_opponent_standard(self):
        text = "相手の モジャンボの\nリーフストーム!"
        matches, line_consumed, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertTrue(event.is_opponent)
        self.assertTrue("リーフストーム", event.move)

    def test_ally_used(self):
        text = "モジャンボは\nはたきおとすを つかった!"
        matches, line_consumed, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertFalse(event.is_opponent)
        self.assertTrue("はたきおとす", event.move)

    def test_opponent_used(self):
        text = "相手の モジャンボは\nはたきおとすを つかった!"
        matches, line_consumed, event = matcher.matches(text, Locale.JA)
        self.assertTrue(matches)
        self.assertEqual(line_consumed, 2)
        self.assertEqual("モジャンボ", event.pokemon)
        self.assertEqual(text, event.message)
        self.assertTrue(event.is_opponent)
        self.assertTrue("はたきおとす", event.move)
