import csv
from typing import List


def load_pokemon_dictionary(path: str) -> List[str]:
    result = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["local_language_id"] != "11":
                continue
            result.append(row["name"])

    return result
