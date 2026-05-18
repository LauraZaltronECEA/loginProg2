
from business.LoginHelper import LoginHelper
from presentation.account import Account
from getpass import getpass
from data.entitiy.LoggedUser import LoggedUser

class Login:

    def __init__(self):
        self.loginHelper = LoginHelper()
        self.account = Account()

    def registrarUsuario(self):
        try:
            username = input("Por favor Ingrese el nuevo nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)

            pwd1 = getpass(prompt="Ingrese el password:\n")
            pwd2 = getpass("Por favor, repita el password:\n")

            self.loginHelper.checkEqPwd(pwd1,pwd2)
            self.loginHelper.prepareAndStorePwd(username,pwd1)
            
            if self.loginHelper.checkUserAndPwd(username, pwd1):
                print("Usuario {} registrado con exito, ya puede iniciar sesion".format(username))  
                self.account.cuenta_ARS_registro(username)
                print("Cuenta en ARS creada automaticamente...")
        except Exception as e:
            print("Error: {}".format(e.args[0]))
    
    def iniciarSesion(self):
        try:
            username = input("Por favor Ingrese el nombre de usuario:\n")

            pwd = getpass(prompt="Ingrese el password:\n")

            self.loginHelper.checkUserAndPwd(username,pwd)

            if self.loginHelper.checkUserAndPwd(username, pwd):
                print("Bienvenido {}".format(username))
                nombreUsuarioObjeto = LoggedUser(username)
                return nombreUsuarioObjeto
            else:
                return None

        except ValueError as e:
            print("Error: {}".format(e.args[0]))

            


