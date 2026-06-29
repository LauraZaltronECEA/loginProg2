from data.repository import Repository
from data.json_repository import JsonRepository
from data.sql_repository import SQLRepository


class RepositoryFactory:

    @staticmethod
    def create_repository(db_type: str) -> Repository:
        if db_type == "json":
            return JsonRepository()
        elif db_type == "sql":
            return SQLRepository()
        else:
            raise ValueError(f"Tipo de repositorio desconocido: '{db_type}'. Use 'json' o 'sql'.")
