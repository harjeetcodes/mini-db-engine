import json

def save_table(table, filename):
    data = {
        "name": table.name,
        "schema": {k: v.__name__ for k, v in table.schema.items()},
        "rows": table.all_rows()
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_table(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    # convert schema strings back to types
    type_map = {"int": int, "str": str, "float": float}
    schema = {k: type_map[v] for k, v in data["schema"].items()}

    from table import Table
    table = Table(data["name"], schema)

    for row in data["rows"]:
        table.insert(row)

    return table
