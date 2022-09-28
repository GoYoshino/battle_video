import os

from pokedex.load_dictionary import load_pokemon_dictionary
from pokedex.reverse_normalization_dictionary import create_reverse_normalization_dictionary

def get_path(rel_path: str):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, rel_path)

class Pokedex:

    def __init__(self):
        self.pokemons = load_pokemon_dictionary(get_path("data/pokemon_species_names.csv"))
        self.pokemons_reverse = create_reverse_normalization_dictionary(self.pokemons)
