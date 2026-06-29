from presentation.auth import Auth
from presentation.account import Account

class Menu:

    def __init__(self, repository):
        self.auth = Auth(repository)
        self.account = Account(repository)

    def menu(self):
        try:
            while True:
                print(20 * '#', "Bienvenido a la Aplicacion", 20 * '#')
                print("Ingrese una Opcion")
                print("1 - Iniciar Sesion")
                print("2 - Crear Usuario")
                print("0 - Salir")

                op = input().strip()
                match op:
                    case '1':
                        user = self.auth.iniciar_sesion()
                        if user is not None:
                            self.menu_usuario(user)
                    case '2':
                        self.auth.registrar_usuario()
                    case '0':
                        print("Saliendo de la Aplicacion...")
                        break
                    case _:
                        print("Opcion Incorrecta")
        except Exception as e:
            print(e)

    def menu_usuario(self, user):
        try:
            while True:
                print(20 * '#', "Menu de Usuario", 20 * '#')
                print("Ingrese una Opcion")
                print("1 - Abrir Cuenta Nueva")
                print("2 - Listar Cuentas y Saldos")
                print("3 - Ingresar Pesos Argentinos")
                print("4 - Ingresar Moneda Extranjera")
                print("5 - Exportar Resumen de Cuentas")
                print("0 - Cerrar Sesion")
                op = input().strip()
                match op:
                    case '1':
                        self.account.abrir_cuenta(user.get_username())
                    case '2':
                        self.account.listar_cuentas(user.get_username())
                    case '3':
                        self.account.ingresar_pesos_argentinos(user.get_username())
                    case '4':
                        self.account.ingresar_moneda_extranjera(user.get_username())
                    case '5':
                        self.account.exportar_resumen(user.get_username())
                    case '0':
                        print("Cerrando Sesion...")
                        break
                    case _:
                        print("Opcion Incorrecta")
        except Exception as e:
            print(e)
