from business.dataHelper import DataHelper
from business.APIHelper import APIHelper
from decimal import Decimal

class AccountHelper:
    def __init__(self):
        self.dataHelper = DataHelper()
        self.apiHelper = APIHelper()
        self.validCurrencies = self.apiHelper.getSymbols()

    def checkCurrency(self, currency):
        currency = currency.upper().strip()
        if len(currency) != 3:
            raise ValueError("La moneda debe tener exactamente 3 letras")
        if currency not in self.validCurrencies:
            raise ValueError("Moneda no valida")
        return currency

    def checkDecimal(self, amount):
        try:
            amount = Decimal(amount)
            if amount < 0:
                raise ValueError("El monto no puede ser negativo")
            return amount
        except:
            raise ValueError("Monto no valido, debe ser un numero decimal")

    def crear_cuenta(self, username, moneda):
        moneda = self.checkCurrency(moneda)
        accounts = self.dataHelper.loadUserAccounts(username)
        if moneda in accounts:
            raise ValueError(f"Ya existe una cuenta en {moneda}")
        accounts[moneda] = str(Decimal('0'))
        self.dataHelper.saveUserAccounts(username, accounts)

    def get_cuentas(self, username):
        return self.dataHelper.loadUserAccounts(username)
    
    def calcTotal_CheckBalanceARS(self, foreign_currency, amount):
        try:
            totalAmount_exchange_ars_to_foreign = self.apiHelper.getTotalAmount_foreign_ars(foreign_currency, amount)
            return totalAmount_exchange_ars_to_foreign
        except Exception as e:
             raise Exception("Error al calcular el monto total en AccountHelper: {}".format(e.args[0]))

    def checkExistingAccount(self, monedaExtranjera, accounts, username):
            
        if monedaExtranjera not in self.apiHelper.getSymbols():
            print("Moneda no soportada. Por favor, intente nuevamente.")
            return False
        elif monedaExtranjera not in accounts:
            print("No tienes una cuenta en {}, Desea crearla? (s/n):".format(monedaExtranjera))
            choice = input().strip().lower()
            if choice == 's':
                self.crear_cuenta(username, monedaExtranjera)
                return True
            else:
                print("Operacion cancelada.")
                return False
        else:
            return True
        
    def accARStoDecimal(self, accounts):
       decimal_ars = Decimal(accounts["ARS"])
       return decimal_ars 
    
    # def getCurrencies(self):
    #     return self.validCurrencies