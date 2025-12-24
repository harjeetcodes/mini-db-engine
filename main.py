from database import Database
from parser import QueryParser
from planner import QueryPlanner
from executor import QueryExecutor
from transaction import TransactionManager
from cli import MiniDBCLI

db = Database()
db.create_table("users", {"id": int, "name": str, "age": int})

users = db.get_table("users")
users.insert({"id": 1, "name": "Aman", "age": 22})
users.insert({"id": 2, "name": "Riya", "age": 17})

users.create_index("age")

parser = QueryParser()
planner = QueryPlanner()
executor = QueryExecutor(db, planner)
tx = TransactionManager(db)

cli = MiniDBCLI(parser, executor, tx)
cli.start()
