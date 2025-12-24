class QueryParser:
    def parse(self, query: str):
        q = query.strip()
        uq = q.upper()

        if uq.startswith("SELECT"):
            return self._parse_select(q)

        if uq.startswith("INSERT"):
            return self._parse_insert(q)

        if uq.startswith("UPDATE"):
            return self._parse_update(q)

        if uq.startswith("DELETE"):
            return self._parse_delete(q)

        raise ValueError("Only SELECT, INSERT, UPDATE, DELETE queries are supported")

    # ---------------- SELECT ----------------
    def _parse_select(self, q):
        parts = q.split()
        fi = parts.index("FROM")

        cols = parts[1:fi]
        columns = ["*"] if cols == ["*"] else "".join(cols).split(",")

        table = parts[fi + 1]

        condition = None
        order_by = None

        if "WHERE" in parts:
            w = parts.index("WHERE")
            condition = (parts[w+1], parts[w+2], parts[w+3].strip('"'))

        if "ORDER" in parts:
            o = parts.index("ORDER")
            order_by = (parts[o+2], parts[o+3] if len(parts) > o+3 else "ASC")

        return {
            "type": "SELECT",
            "table": table,
            "columns": [c.strip() for c in columns],
            "condition": condition,
            "order_by": order_by
        }

    # ---------------- INSERT ----------------
    def _parse_insert(self, q):
        table = q.split()[2]
        raw = q[q.index("(")+1:q.index(")")]
        values = [v.strip().strip('"') for v in raw.split(",")]

        return {
            "type": "INSERT",
            "table": table,
            "values": values
        }

    # ---------------- UPDATE ----------------
    def _parse_update(self, q):
        parts = q.split()
        table = parts[1]

        si = parts.index("SET")
        wi = parts.index("WHERE") if "WHERE" in parts else None

        set_expr = " ".join(parts[si+1:wi])
        col, val = set_expr.split("=")

        condition = None
        if wi:
            c = parts[wi+1:]
            condition = (c[0], c[1], c[2].strip('"'))

        return {
            "type": "UPDATE",
            "table": table,
            "set": (col.strip(), val.strip().strip('"')),
            "condition": condition
        }

    # ---------------- DELETE ----------------
    def _parse_delete(self, q):
        parts = q.split()
        table = parts[2]

        condition = None
        if "WHERE" in parts:
            w = parts.index("WHERE")
            condition = (parts[w+1], parts[w+2], parts[w+3].strip('"'))

        return {
            "type": "DELETE",
            "table": table,
            "condition": condition
        }
