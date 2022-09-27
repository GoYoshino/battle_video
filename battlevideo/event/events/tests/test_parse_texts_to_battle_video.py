from unittest import TestCase

from battlevideo import parse_texts_to_battle_video
from battlevideo.event.events import OpponentPokemonSentEvent


class ParseTextsToBattleVideoTest(TestCase):

    def test_accepts_kuridasi_text(self):
        texts = ["レッドは\nピカチュウを くりだした!", "通信待機中..."]
        video = parse_texts_to_battle_video(texts)

        sent_event: OpponentPokemonSentEvent = video[0]
        self.assertEqual("レッドは\nピカチュウを くりだした!", sent_event.message)
        self.assertIsInstance(sent_event, OpponentPokemonSentEvent)
        self.assertEqual("ピカチュウ", sent_event.pokemon)

    def test_ignores_series_of_same_texts(self):
        # メモ： ここの仕様について→「同じ技を繰り出す」が偶然連続した場合、個別のイベントとして扱えない可能性がある
        # 将来的に「HP減少イベント」と組み合わせることでそういうことは一応なくなる。

        texts = [
            "レッドは\nピカチュウを くりだした!",
            "レッドは\nピカチュウを くりだした!",
            "ゆけっ! ザシアン!",
            "ゆけっ! ザシアン!",
            "通信待機中...",
            "レッドは\nピカチュウを くりだした!"
        ]
        video = parse_texts_to_battle_video(texts)

        self.assertEqual(len(video), 3)
        self.assertEqual(video[0].message, "レッドは\nピカチュウを くりだした!")
        self.assertEqual(video[1].message, "ゆけっ! ザシアン!")
        self.assertEqual(video[2].message, "レッドは\nピカチュウを くりだした!")
