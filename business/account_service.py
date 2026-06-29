from decimal import Decimal
import bcrypt
from data.repository import Repository
from infrastructure.api_service import ApiService

class AccountService:

    def __init__(self, repository: Repository):
        self.repository = repository
        self.api_service = ApiService()
        self.valid_currencies = self.api_service.get_symbols()

    def check_currency(self, currency):
        currency = currency.upper().strip()
        if len(currency) != 3:
            raise ValueError("La moneda debe tener exactamente 3 letras")
        if currency not in self.valid_currencies:
            raise ValueError("Moneda no valida")
        return currency

    def check_decimal(self, amount):
        amount = Decimal(amount)
        if amount < 0:
            raise ValueError("El monto no puede ser negativo")
        return amount

    def create_account(self, username, currency):
        currency = self.check_currency(currency)
        accounts = self.repository.load_user_accounts(username)
        if currency in accounts:
            raise ValueError(f"Ya existe una cuenta en {currency}")
        accounts[currency] = str(Decimal('0'))
        self.repository.save_user_accounts(username, accounts)

    def get_accounts(self, username):
        return self.repository.load_user_accounts(username)

    def calc_exchange_rate(self, foreign_currency, amount):
        return self.api_service.get_total_amount_foreign_ars(foreign_currency, amount)

    def check_pwd(self, username, clave):
        hashed = self.repository.get_user(username)
        if hashed is None:
            return False
        return bcrypt.checkpw(clave.encode('utf-8'), hashed.encode('utf-8'))

    def is_currency_valid(self, currency):
        return currency.upper().strip() in self.valid_currencies

    def has_account(self, username, currency):
        accounts = self.repository.load_user_accounts(username)
        return currency in accounts

    def save_accounts(self, username, accounts):
        return self.repository.save_user_accounts(username, accounts)
