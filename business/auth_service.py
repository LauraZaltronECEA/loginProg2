import re
import bcrypt
from data.repository import Repository

class AuthService:

    def __init__(self, repository: Repository):
        self.repository = repository

    def sanitize(self, text):
        if not isinstance(text, str):
            raise TypeError("El texto debe ser una cadena")

        sanitized = text.strip().lower()
        sanitized = re.sub(r"\s+", "", sanitized)
        sanitized = re.sub(r"[^a-z0-9_-]", "", sanitized)

        if not sanitized:
            raise ValueError("El nombre de usuario no puede estar compuesto por caracteres inválidos.")

        return sanitized

    def check_eq_pwd(self, pwd1, pwd2):
        if pwd1 != pwd2:
            raise ValueError("Las passwords no coinciden")

    def prepare_and_store_pwd(self, username, pwd):
        coded = pwd.encode('utf-8')
        hashed = bcrypt.hashpw(coded, bcrypt.gensalt())
        self.repository.add_user(username, hashed.decode('utf-8'))

    def check_user_and_pwd(self, username, pwd):
        hashed = self.repository.get_user(username)
        if hashed is None:
            raise ValueError("Usuario invalido")
        if bcrypt.checkpw(pwd.encode('utf-8'), hashed.encode('utf-8')):
            return True
        raise ValueError("Password Incorrecto")

    def check_existing_user(self, username):
        return self.repository.get_user(username) is not None
