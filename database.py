class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, schema):
        from table import Table
        self.tables[name] = Table(name, schema)

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")
        return self.tables[name]
