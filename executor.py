class QueryExecutor:
    def __init__(self, database, planner):
        self.database = database
        self.planner = planner

    # ---------------- ENTRY POINT ----------------
    def execute(self, query):
        t = query["type"]

        if t == "SELECT":
            return self._select(query)
        if t == "INSERT":
            return self._insert(query)
        if t == "UPDATE":
            return self._update(query)
        if t == "DELETE":
            return self._delete(query)

        raise ValueError("Unknown query type")

    # ---------------- HELPERS ----------------
    def _match(self, row, condition):
        if condition is None:
            return True

        col, op, val = condition
        cell = row.get(col)
        val = int(val) if val.isdigit() else val

        if op == ">":
            return cell > val
        if op == "<":
            return cell < val
        if op == "==":
            return cell == val

        raise ValueError("Unsupported operator")

    # ---------------- SELECT ----------------
    def _select(self, q):
        table = self.database.get_table(q["table"])
        condition = q["condition"]

        plan = self.planner.choose_plan(table, condition)

        if plan == "INDEX":
            col, _, val = condition
            val = int(val) if val.isdigit() else val
            rows = table._indexes[col].get(val, [])
        else:
            rows = [r for r in table._rows if self._match(r, condition)]

        if q["order_by"]:
            col, direction = q["order_by"]
            rows = sorted(
                rows,
                key=lambda r: r.get(col),
                reverse=(direction == "DESC")
            )

        if q["columns"] == ["*"]:
            return [r.as_dict() for r in rows]

        return [{c: r.get(c) for c in q["columns"]} for r in rows]

    # ---------------- INSERT ----------------
    def _insert(self, q):
        table = self.database.get_table(q["table"])
        keys = list(table.schema.keys())

        data = {}
        for key, val in zip(keys, q["values"]):
            data[key] = table.schema[key](val)

        table.insert(data)
        return "Inserted 1 row"

    # ---------------- UPDATE ----------------
    def _update(self, q):
        table = self.database.get_table(q["table"])
        col, val = q["set"]
        val = table.schema[col](val)

        count = 0
        for row in table._rows:
            if self._match(row, q["condition"]):
                row.set(col, val)
                count += 1

        return f"Updated {count} rows"

    # ---------------- DELETE ----------------
    def _delete(self, q):
        table = self.database.get_table(q["table"])
        before = len(table._rows)

        table._rows = [
            r for r in table._rows
            if not self._match(r, q["condition"])
        ]

        return f"Deleted {before - len(table._rows)} rows"
