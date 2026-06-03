import json

FILE_PATH = "src/data/inventory.json"

def load_inventory():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_inventory(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)