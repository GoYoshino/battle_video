from battlevideo.event.events import Event


class BattleState:
    
    def __init__(self, event: Event, ally_pokemon_left: int, opponent_pokemons_left: int):
        self.event = event
        self.ally_pokemon_left = ally_pokemon_left
        self.opponent_pokemons_left = opponent_pokemons_left

    def __repr__(self):
        return self.event.__repr__()
