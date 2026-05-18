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

    def cuenta_ARS_registro(self, username):
        try:
            self.accountHelper.crear_cuenta(username, "ARS")
        except Exception as e:
            print("Error: {}".format(e.args[0]))

    def ingresar_pesos_argentinos(self, username):
            try:
                if "ARS" not in self.accountHelper.get_cuentas(username):
                    print("No tienes una cuenta en ARS, creando una automaticamente para seguir operando...")
                    self.cuenta_ARS_registro(username)

                amount = input("Ingrese el monto en pesos argentinos:\n")
                amount = self.accountHelper.checkDecimal(amount)

                accounts = self.accountHelper.get_cuentas(username)
                current_balance = self.accountHelper.checkDecimal(accounts["ARS"])
                new_balance = current_balance + amount

                accounts["ARS"] = str(new_balance)
                if self.accountHelper.dataHelper.saveUserAccounts(username, accounts):
                    print("Monto ingresado exitosamente. Nuevo saldo en ARS: {}".format(new_balance))
                else:
                    print("Error al guardar el nuevo saldo.")
                    
            except Exception as e:
                print("Error: {}".format(e.args[0]))

    # def getAllCurrencies(self):
    #     print("Monedas disponibles:")
    #     for currency in self.accountHelper.getCurrencies():
    #         print(currency)
