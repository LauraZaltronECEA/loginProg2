from business.AccountHelper import AccountHelper
import tabulate
class Account:

    def __init__(self):
        self.accountHelper = AccountHelper()

    def abrir_cuenta(self, username):
        try:
            moneda = input("Ingrese el codigo de moneda (3 letras, ej: USD):\n")
            self.accountHelper.crear_cuenta(username, moneda)
            print("Cuenta en {} creada con exito".format(moneda.upper()))
        except Exception as e:
            print("Error: {}".format(e.args[0]))

    def listar_cuentas(self, username):
        try:
            accounts = self.accountHelper.get_cuentas(username)
            if not accounts:
                print("No hay cuentas abiertas")
                return
            
            tabulate_data = [[moneda, saldo] for moneda, saldo in accounts.items()]
            print(tabulate.tabulate(tabulate_data, headers=["Moneda", "Saldo"], tablefmt="grid"))

        except Exception as e:
            print("Error: {}".format(e.args[0]))
