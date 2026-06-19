import json

FILE_PATH = "src/data/supply_chain.json"


def load_supply_chain():
    with open(FILE_PATH, "r") as f:
        return json.load(f)