from battlevideo.event.events import Event


class BattleEndedEvent(Event):

    def __init__(self, winner_is_opponent: bool):
        message = "相手の勝ち" if winner_is_opponent else "自分の勝ち"
        super().__init__(message)
        self.is_opponent = winner_is_opponent
