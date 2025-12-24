import json
from database import Database

TYPE_MAP = {"int": int, "str": str, "float": float}

def save_db(db, filename):
    with open(filename, "w") as f:
        json.dump(db.to_dict(), f, indent=4)

def load_db(filename):
    with open(filename) as f:
        raw = json.load(f)

    db = Database()
    for table_name, data in raw.items():
        schema = {k: TYPE_MAP[v] for k, v in data["schema"].items()}
        db.create_table(table_name, schema)
        table = db.get_table(table_name)
        for row in data["rows"]:
            table.insert(row)

    return db
