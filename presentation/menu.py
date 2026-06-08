from presentation.login import Login
from presentation.account import Account

class Menu:

    def __init__(self):
        self.login = Login()
        self.account = Account()

    def menu(self):
        print(20*'#', "Bienvenido a la Aplicacion",20*'#')
        print("Ingrese una Opcion")
        print("1 - Iniciar Sesion")
        print("2 - Crear Usuario")
        print("0 - Salir")
        
        op = input().strip()
        match op:
            case '1':
                user = self.login.iniciarSesion()
                if user is not None:
                    self.menu_usuario(user)
            case '2':
                self.login.registrarUsuario()
            case '0':
                return print("Saliendo de la Aplicacion...")
            case _:
                print("Opcion Incorrecta")
                return self.menu()
            
    def menu_usuario(self, user):
        print(20*'#', "Menu de Usuario",20*'#')
        print("Ingrese una Opcion")
        print("1 - Abrir Cuenta Nueva")
        print("2 - Listar Cuentas y Saldos")
        print("3 - Ingresar Pesos Argentinos")
        print("4 - Ingresar Moneda Extranjera")
        print("0 - Salir")
        op = input().lstrip().rstrip()
        match op:
            case '1':
                self.account.abrir_cuenta(user.getUsername())
                return self.menu_usuario(user)
            case '2':
                self.account.listar_cuentas(user.getUsername())
                return self.menu_usuario(user)
            case '3':
                self.account.ingresar_pesos_argentinos(user.getUsername())
                return self.menu_usuario(user)
            case '4':
                self.account.ingresar_moneda_extranjera(user.getUsername())
                return self.menu_usuario(user)
            case '5':
                self.account.consultar_saldo(user.getUsername())
                return self.menu_usuario(user)
            case '0':
                return print("Cerrando Sesion...")
            case _:
                print("Opcion Incorrecta")
                return self.menu_usuario(user)
