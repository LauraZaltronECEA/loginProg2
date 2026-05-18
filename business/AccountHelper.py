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
    
    def getCurrencies(self):
        return self.validCurrencies