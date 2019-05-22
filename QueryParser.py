from fuzzywuzzy import fuzz
import sqlite3


class QueryParser():

    def __init__(self):
        conn = sqlite3.connect('./data/PokemonShuffle.db')
        c = conn.cursor()
        self.skill_list = [skill[0] for skill in c.execute("select Name from skill_table").fetchall()]
        self.pokemon_list = [pokemon[0].lower() for pokemon in c.execute("select Name from pokedex").fetchall()]
        self.type_list = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
        return

    def parse_pokemon(self, name):
        ratios = {}
        for n in self.pokemon_list:
            r = fuzz.ratio(n, name)
            ratios[n] = r
        return max(ratios, key=lambda key: ratios[key])

    def parse_skill(self, name):
        ratios = {}
        for n in self.skill_list:
            r = fuzz.ratio(n, name)
            ratios[n] = r
        return max(ratios, key=lambda key: ratios[key])

    def parse_type(self, name):
        ratios = {}
        for n in self.type_list:
            r = fuzz.ratio(n, name)
            ratios[n] = r
        return max(ratios, key=lambda key: ratios[key])

    def parse_number(self, number):
        try:
            number = int(number)
        except Exception:
            number = 0
        return number
