from business.auth_service import AuthService
from presentation.account import Account
from getpass import getpass
from business.logged_user import LoggedUser

class Auth:

    def __init__(self, repository):
        self.auth_service = AuthService(repository)
        self.account = Account(repository)

    def registrar_usuario(self):
        try:
            username = input("Por favor Ingrese el nuevo nombre de usuario:\n")
            username = self.auth_service.sanitize(username)

            if self.auth_service.check_existing_user(username):
                raise ValueError("Nombre de usuario NO disponible, por favor elija otro")

            pwd1 = getpass(prompt="Ingrese el password:\n")
            pwd2 = getpass("Por favor, repita el password:\n")

            self.auth_service.check_eq_pwd(pwd1, pwd2)
            self.auth_service.prepare_and_store_pwd(username, pwd1)

            if self.auth_service.check_user_and_pwd(username, pwd1):
                print(f"Usuario {username} registrado con exito, ya puede iniciar sesion")
                self.account.cuenta_ars_registro(username)
                print("Cuenta en ARS creada automaticamente...")
        except Exception as e:
            print(e)

    def iniciar_sesion(self):
        try:
            username = input("Por favor Ingrese el nombre de usuario:\n")
            pwd = getpass(prompt="Ingrese el password:\n")
            self.auth_service.check_user_and_pwd(username, pwd)
            print(f"Bienvenido {username}")
            return LoggedUser(username)
        except Exception as e:
            print(e)
            return None
