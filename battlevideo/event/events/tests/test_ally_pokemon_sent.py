from unittest import TestCase

from battlevideo.event.events.ally_pokemon_sent import AllyPokemonSentMatcher
from battlevideo.event.locale import Locale
from pokedex.pokedex import Pokedex

matcher = AllyPokemonSentMatcher(Pokedex())

class AllyPokemonSentMatcherTest(TestCase):

    def test_other_message_does_not_match(self):
        matches, event = matcher.matches("ウオノラゴンは\nゴツゴツメットで ダメージを受けた!", Locale.JA)
        self.assertFalse(matches)

    def test_type1_matches(self):
        matches, event = matcher.matches("ゆけっ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("ゆけっ! ウオノラゴン!", event.message)

    def test_type1_works_with_titled_pokemon(self):
        matches, event = matcher.matches("ゆけっ! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("ゆけっ! ウオノラゴン!", event.message)

    def test_type2_matches(self):
        matches, event = matcher.matches("任せた! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("任せた! ウオノラゴン!", event.message)

    def test_type2_works_with_titled_pokemon(self):
        matches, event = matcher.matches("任せた! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("任せた! ウオノラゴン!", event.message)

    def test_type3_matches(self):
        matches, event = matcher.matches("相手が 弱っている!\nチャンスだ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("相手が 弱っている!\nチャンスだ! ウオノラゴン!", event.message)

    def test_type3_works_with_titled_pokemon(self):
        matches, event = matcher.matches("相手が 弱っている!\nチャンスだ! ガラルチャンピオン ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)
        self.assertEqual("相手が 弱っている!\nチャンスだ! ウオノラゴン!", event.message)

    ### normalization ###
    def test_type1_does_normalized_match_for_text_base(self):
        matches, event = matcher.matches("ゆけつ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)

    def test_type1_revises_text_base(self):
        matches, event = matcher.matches("ゆけつ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ゆけっ! ウオノラゴン!", event.message)

    def test_type1_does_normalized_match_for_pokemon_name(self):
        matches, event = matcher.matches("ゆけつ! モジヤンボ!", Locale.JA)
        self.assertTrue(matches)

    def test_type1_revises_pokemon_name(self):
        matches, event = matcher.matches("ゆけつ! モジヤンボ!", Locale.JA)
        self.assertEqual("ゆけっ! モジャンボ!", event.message)

    def test_type2_does_normalized_match_for_pokemon_name(self):
        matches, event = matcher.matches("任せた! モジヤンボ!", Locale.JA)
        self.assertTrue(matches)

    def test_type2_revises_pokemon_name(self):
        matches, event = matcher.matches("任せた! モジヤンボ!", Locale.JA)
        self.assertEqual("任せた! モジャンボ!", event.message)

    def test_type3_does_normalized_match_for_text_base_former(self):
        matches, event = matcher.matches("相手が 弱つている!\nチャンスだ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_type3_revises_text_base_former(self):
        matches, event = matcher.matches("相手が 弱つている!\nチャンスだ! ウオノラゴン!", Locale.JA)
        self.assertEqual("相手が 弱っている!\nチャンスだ! ウオノラゴン!", event.message)

    def test_type3_does_normalized_match_for_text_base_latter(self):
        matches, event = matcher.matches("相手が 弱っている!\nチヤンスだ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_type3_revises_text_base_latter(self):
        matches, event = matcher.matches("相手が 弱っている!\nチヤンスだ! ウオノラゴン!", Locale.JA)
        self.assertEqual("相手が 弱っている!\nチャンスだ! ウオノラゴン!", event.message)

    def test_type3_does_normalized_match_for_text_base_both(self):
        matches, event = matcher.matches("相手が 弱つている!\nチヤンスだ! ウオノラゴン!", Locale.JA)
        self.assertTrue(matches)
        self.assertEqual("ウオノラゴン", event.pokemon)

    def test_type3_revises_text_base_both(self):
        matches, event = matcher.matches("相手が 弱つている!\nチヤンスだ! ウオノラゴン!", Locale.JA)
        self.assertEqual("相手が 弱っている!\nチャンスだ! ウオノラゴン!", event.message)

    def test_type3_does_normalized_match_for_pokemon_name(self):
        matches, event = matcher.matches("相手が 弱つている!\nチャンスだ! モジヤンボ!", Locale.JA)
        self.assertTrue(matches)

    def test_type3_revises_pokemon_name(self):
        matches, event = matcher.matches("相手が 弱つている!\nチャンスだ! モジヤンボ!", Locale.JA)
        self.assertEqual("相手が 弱っている!\nチャンスだ! モジャンボ!", event.message)


    ### ビックリマーク関連: 仕様にするか未定。実際に上がってくるOCRデータを見て決めたい ###
    def test_type1_tolerates_lost_exclamation_mark_former(self):
        pass

    def test_type1_tolerates_lost_exclamation_mark_latter(self):
        pass

    def test_type1_tolerates_lost_exclamation_mark_both(self):
        pass

    def test_type1_revises_lost_exclamation_mark(self):
        pass

    def test_type2_tolerates_lost_exclamation_mark_former(self):
        pass

    def test_type2_tolerates_lost_exclamation_mark_latter(self):
        pass

    def test_type2_tolerates_lost_exclamation_mark_both(self):
        pass

    def test_type2_revises_lost_exclamation_mark(self):
        pass

    def test_type3_tolerates_lost_exclamation_mark_former(self):
        pass

    def test_type3_tolerates_lost_exclamation_mark_latter(self):
        pass

    def test_type3_tolerates_lost_exclamation_mark_both(self):
        pass

    def test_type3_revises_lost_exclamation_mark(self):
        pass

