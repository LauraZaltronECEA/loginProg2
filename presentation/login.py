from business.LoginHelper import LoginHelper
from getpass import getpass
from data.entitiy.User import User
class Login:

    def __init__(self):
        self.loginHelper = LoginHelper()

    def registrarUsuario(self):
        try:
            username = input("Por favor Ingrese el nuevo nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)

            pwd1 = getpass(prompt="Ingrese el password:\n")
            pwd2 = getpass("Por favor, repita el password:\n")

            self.loginHelper.checkEqPwd(pwd1,pwd2)
            self.loginHelper.prepareAndStorePwd(username,pwd1)

            print("Usuario {} registrado con exito, ya puede iniciar sesion".format(username))
        except Exception as e:
            print("Error: {}".format(e.args[0]))
    
    def iniciarSesion(self):
        try:
            username = input("Por favor Ingrese el nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)

            pwd = getpass(prompt="Ingrese el password:\n")

            self.loginHelper.checkUserAndPwd(username,pwd)

            print("Bienvendo {}".format(username))

            nombreUsuarioObjeto = User(username)
            
            return  nombreUsuarioObjeto
        except ValueError as e:
            print("Error: {}".format(e.args[0]))

            


