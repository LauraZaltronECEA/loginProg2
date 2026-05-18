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