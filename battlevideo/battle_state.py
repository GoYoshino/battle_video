from battlevideo.event.events import Event


class BattleState:

    def __init__(self, ally_pokemons_left: int, opponent_pokemons_left: int):
        self.ally_pokemons_left = ally_pokemons_left
        self.opponent_pokemons_left = opponent_pokemons_left

    def __repr__(self):
        return f"相手残り: {self.opponent_pokemons_left}, 自分残り={self.ally_pokemons_left}"
