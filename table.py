from row import Row
from collections import defaultdict

class Table:
    def __init__(self, name: str, schema: dict):
        self.name = name
        self.schema = schema
        self._rows = []
        self._indexes = {}  # column -> {value: [rows]}

    # ---------------- INDEXING ----------------
    def create_index(self, column: str):
        if column not in self.schema:
            raise ValueError(f"Cannot create index on unknown column '{column}'")

        index = defaultdict(list)
        for row in self._rows:
            index[row.get(column)].append(row)

        self._indexes[column] = index

    def _update_indexes_on_insert(self, row):
        for col, index in self._indexes.items():
            index[row.get(col)].append(row)

    # ---------------- CORE OPS ----------------
    def insert(self, values: dict):
        self._validate(values)
        row = Row(values)
        self._rows.append(row)
        self._update_indexes_on_insert(row)

    def select(self, condition=None):
        if condition is None:
            return list(self._rows)
        return [row for row in self._rows if condition(row)]

    def all_rows(self):
        return [r.as_dict() for r in self._rows]

    # ---------------- VALIDATION ----------------
    def _validate(self, values):
        for col, typ in self.schema.items():
            if col not in values:
                raise ValueError(f"Missing column: {col}")
            if not isinstance(values[col], typ):
                raise TypeError(f"{col} must be {typ.__name__}")
