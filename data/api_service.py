from decimal import Decimal
import os
import dotenv
import requests


class ApiService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        dotenv.load_dotenv()
        self.api_key = os.getenv("FIXER_API_KEY")
        self.base_url = "http://data.fixer.io/"
        self.symbols = []
        self._initialized = True

    def get_symbols(self):
        if self.symbols:
            return self.symbols
        url = f"{self.base_url}api/symbols?access_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                self.symbols = list(data["symbols"].keys())
                return self.symbols
            raise Exception("Error en la respuesta de la API: " + data.get("error", {}).get("info", ""))
        raise Exception(f"Error al conectar con la API: {response.status_code}")

    def get_all_latest_rate_eur(self):
        url = f"{self.base_url}api/latest?access_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["rates"]
            raise Exception("Error en la respuesta de la API: " + data.get("error", {}).get("info", ""))
        raise Exception(f"Error al conectar con la API: {response.status_code}")

    def get_total_amount_foreign_ars(self, foreign_currency, amount):
        latest_rates = self.get_all_latest_rate_eur()
        rate_foreign = latest_rates.get(foreign_currency)
        rate_ars = latest_rates.get("ARS")
        exchange_rate_ars = Decimal(str(rate_ars)) / Decimal(str(rate_foreign))
        return amount * exchange_rate_ars
