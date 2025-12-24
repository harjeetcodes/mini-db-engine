class Row:
    def __init__(self, data: dict):
        self._data = data.copy()

    def get(self, column):
        return self._data.get(column)

    def set(self, column, value):
        self._data[column] = value

    def as_dict(self):
        return self._data.copy()

    def __repr__(self):
        return f"Row({self._data})"
