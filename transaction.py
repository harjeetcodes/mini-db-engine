import copy

class TransactionManager:
    def __init__(self, database):
        self.database = database
        self._snapshot = None

    def begin(self):
        if self._snapshot is not None:
            raise RuntimeError("Transaction already started")
        self._snapshot = copy.deepcopy(self.database.tables)

    def rollback(self):
        if self._snapshot is None:
            raise RuntimeError("No active transaction")
        self.database.tables = self._snapshot
        self._snapshot = None

    def commit(self):
        if self._snapshot is None:
            raise RuntimeError("No active transaction")
        self._snapshot = None
