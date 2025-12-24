class QueryPlanner:
    def choose_plan(self, table, condition):
        if not condition:
            return "FULL_SCAN"

        col, op, _ = condition
        if op == "==" and col in table._indexes:
            return "INDEX"
        return "FULL_SCAN"
