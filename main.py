import os
import dotenv
from presentation.menu import Menu

dotenv.load_dotenv()
db_type = os.getenv("DB_TYPE", "json")

if db_type == "sql":
    from data.sql_repository import SQLRepository
    repo = SQLRepository()
else:
    from data.json_repository import JsonRepository
    repo = JsonRepository()

login = Menu(repo)
login.menu()
