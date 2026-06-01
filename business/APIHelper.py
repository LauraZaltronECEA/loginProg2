from decimal import Decimal
import os
import dotenv
import requests

class APIHelper:

    _instance = None #variable de clase para almacenar la instancia única de la clase

    def __new__(cls):
        
        if cls._instance is None:
            cls._instance = super().__new__(cls) #si no existe una instancia, se crea una nueva instancia de la clase
            cls._instance._initialized = False #se inicializa una lista vacía para almacenar los symbols
        return cls._instance #si ya existe una instancia, se devuelve la instancia existente
    
    def __init__(self):
        if self._initialized: #si la instancia ya ha sido inicializada, no se vuelve a inicializar
            return
        dotenv.load_dotenv()
        self.api_key = os.getenv("FIXER_API_KEY") 
        self.base_url = "http://data.fixer.io/"
        self.symbols = []
        self._initialized = True

    def getSymbols(self):
        if self.symbols:
            return self.symbols
        else:
            url = f"{self.base_url}api/symbols?access_key={self.api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    self.symbols = list(data["symbols"].keys())
                    return self.symbols
                else:
                    raise Exception("Error en la respuesta de la API: " + data.get("error", {}).get("info", ""))
            else:
                raise Exception(f"Error al conectar con la API: {response.status_code}")
            
    def getAllLatestRateEUR(self):
        url = f"{self.base_url}api/latest?access_key={self.api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["rates"]
            else:
                raise Exception("Error en la respuesta de la API: " + data.get("error", {}).get("info", ""))
        else:
            raise Exception(f"Error al conectar con la API: {response.status_code}")
            
    def getTotalAmount_foreign_ars(self, foreign_currency, amount):
        # Obtener las últimas tasas de cambio en relación al euro y convertir 
        # el monto de la moneda extranjera a ARS utilizando el euro como intermediario
        latest_rates = self.getAllLatestRateEUR()
        rate_foreign = latest_rates.get(foreign_currency)
        rate_ars = latest_rates.get("ARS")

        exchange_rate_ars = Decimal(str(rate_ars)) / Decimal(str(rate_foreign))
        return amount * exchange_rate_ars
