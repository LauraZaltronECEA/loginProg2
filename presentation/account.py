from decimal import Decimal

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
            print("Error en account.py abrir_cuenta: {}".format(e.args[0]))

    def listar_cuentas(self, username):
        try:
            accounts = self.accountHelper.get_cuentas(username)
            if not accounts:
                print("No hay cuentas abiertas")
                return
            

            tabulate_data = [[moneda, saldo] for moneda, saldo in accounts.items()]
            
            #hacer que saldo se muestre con 2 decimales

            print(tabulate.tabulate(tabulate_data, headers=["Moneda", "Saldo"], tablefmt="grid"))

            self.menu_opciones_listarcuenta(username)

        except Exception as e:
            print("Error en account.py listar_cuentas: {}".format(e.args[0]))

    def menu_opciones_listarcuenta(self, username):
        try:
            print("1. Volver al Menu")
            print("2. Informacion de la cuenta")
            print("3. abrir cuenta nueva")   
            respuesta = input("Ingrese una opción:")
            match respuesta.strip().lower():
                case '1':
                    return
                case '2':
                    clave = input("Ingrese su contraseña para mostrar la información de la cuenta: ")
                    if self.accountHelper.checkPwd(username, clave):
                        print("...Obteniendo información de la cuenta...")
                case '3':
                    self.abrir_cuenta(username)
                    return
                case _: 
                    print("Opción incorrecta")
        except Exception as e:
                print("Error en account.py listar_cuentas: {}".format(e.args[0]))
        

    def cuenta_ARS_registro(self, username):
        try:
            self.accountHelper.crear_cuenta(username, "ARS")
        except Exception as e:
            print("Error en account.py cuenta_ARS_registro: {}".format(e.args[0]))

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

                str_balance = str(new_balance.quantize(Decimal('0.01')))
                accounts["ARS"] = str(new_balance)
                if self.accountHelper.dataHelper.saveUserAccounts(username, accounts):
                    print("Monto ingresado exitosamente. Nuevo saldo en ARS: {}".format(str_balance))
                else:
                    print("Error al guardar el nuevo saldo.")
                    
            except Exception as e:
                print("Error en account.py ingresar_pesos_argentinos: {}".format(e.args[0]))

    # def getAllCurrencies(self):
    #     print("Monedas disponibles:")
    #     for currency in self.accountHelper.getCurrencies():
    #         print(currency)

    def ingresar_moneda_extranjera(self, username):
        try:
            accounts = self.accountHelper.get_cuentas(username)

            print("Ingrese el codigo de moneda extranjera (3 letras, ej: USD):")
            monedaExtranjera = input().strip().upper()

            exists = self.accountHelper.checkExistingAccount(monedaExtranjera, accounts, username)
            
            if not exists:
                print("Volviendo al Menu de Usuario...")
            else:
                amount = input("Ingrese el monto en {}:\n".format(monedaExtranjera))
                amount = self.accountHelper.checkDecimal(amount)

                totalAmount_exchange_ars_to_foreign = self.accountHelper.calcTotal_CheckBalanceARS(monedaExtranjera, amount)

                ars_Decimal = self.accountHelper.accARStoDecimal(accounts)

                if ars_Decimal < totalAmount_exchange_ars_to_foreign:
                    print("No tienes suficiente saldo en ARS para realizar esta operacion. Saldo actual en ARS: {}".format(ars_Decimal))
                    return
                else:
                    accounts["ARS"] = str(self.accountHelper.checkDecimal(accounts["ARS"]) - totalAmount_exchange_ars_to_foreign)
                    accounts[monedaExtranjera] = str(self.accountHelper.checkDecimal(accounts[monedaExtranjera]) + amount)

                    if self.accountHelper.dataHelper.saveUserAccounts(username, accounts):
                        ars = Decimal(accounts["ARS"]).quantize(Decimal('0.01'))
                        foreign = Decimal(accounts[monedaExtranjera]).quantize(Decimal('0.01'))
                        print("Monto ingresado exitosamente. Nuevo saldo en ARS: {}, Nuevo saldo en {}: {}".format(ars, monedaExtranjera, foreign))
                    else:
                        print("Error al guardar el nuevo saldo.")

        except Exception as e:
            print("Error en account.py ingresar_moneda_extranjera: {}".format(e))
