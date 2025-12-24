import json
from database import Database

TYPE_MAP = {"int": int, "str": str}

def save_db(db, filename):
    data = {}
    for name, table in db.tables.items():
        data[name] = {
            "schema": {k: v.__name__ for k, v in table.schema.items()},
            "rows": table.all_rows(),
            "indexes": list(table._indexes.keys())
        }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_db(filename):
    with open(filename) as f:
        raw = json.load(f)

    db = Database()
    for name, info in raw.items():
        schema = {k: TYPE_MAP[v] for k, v in info["schema"].items()}
        db.create_table(name, schema)

        table = db.get_table(name)
        for row in info["rows"]:
            table.insert(row)

        for col in info["indexes"]:
            table.create_index(col)

    return db
