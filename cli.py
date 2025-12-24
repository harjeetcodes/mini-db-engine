class MiniDBCLI:
    def __init__(self, parser, executor, transaction_manager):
        self.parser = parser
        self.executor = executor
        self.tx = transaction_manager
        self.history = []

    def start(self):
        print("Welcome to MiniDB 🚀")
        print("Type 'help' for commands")

        while True:
            cmd = input("mini-db> ").strip()
            if not cmd:
                continue

            self.history.append(cmd)
            lc = cmd.lower()

            # ---------- TRANSACTIONS ----------
            if lc == "begin":
                self.tx.begin()
                print("Transaction started")
                continue

            if lc == "commit":
                self.tx.commit()
                print("Transaction committed")
                continue

            if lc == "rollback":
                self.tx.rollback()
                print("Transaction rolled back")
                continue

            # ---------- META COMMANDS ----------
            if lc == "exit":
                print("Bye 👋")
                break

            if lc == "help":
                print("""
Commands:
  SELECT ...
  INSERT ...
  UPDATE ...
  DELETE ...
  begin | commit | rollback
  tables
  describe <table>
  history
  exit
""")
                continue

            if lc == "tables":
                print(list(self.executor.database.tables.keys()))
                continue

            if lc.startswith("describe"):
                parts = cmd.split()
                if len(parts) != 2:
                    print("Usage: describe <table>")
                    continue
                table = self.executor.database.get_table(parts[1])
                print(table.schema)
                continue

            if lc == "history":
                for i, h in enumerate(self.history):
                    print(i, h)
                continue

            # ---------- SQL QUERIES ----------
            try:
                parsed = self.parser.parse(cmd)
                result = self.executor.execute(parsed)
                print(result)
            except Exception as e:
                print("Error:", e)
