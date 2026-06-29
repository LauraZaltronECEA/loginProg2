import os
import dotenv
from data.repository_factory import RepositoryFactory
from presentation.menu import Menu

dotenv.load_dotenv()
db_type = os.getenv("DB_TYPE")

repo = RepositoryFactory.create_repository(db_type)

login = Menu(repo)
login.menu()
