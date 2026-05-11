import re #libreria Regular Expressions para poder limpiar el texto de entrada
import bcrypt #libreria para hashear las passwords, es una de las mejores opciones para esto, ya que tiene un algoritmo de hashing fuerte y es fácil de usar
from data.dataHelper import DataHelper

class LoginHelper:

    def __init__(self):
        self.dataHelper = DataHelper()

    def sanitize(self, text):
        if not isinstance(text, str):#Si es distinto a string, tiramos un error de tipo
            raise TypeError("El texto debe ser una cadena")

        sanitizedText = text.strip().lower()
        sanitizedText = re.sub(r"\s+", "", sanitizedText) #elimina espacios en blanco, tabs, etc. y los reemplaza por nada
        sanitizedText = re.sub(r"[^a-z0-9_-]", "", sanitizedText)#elimina caracteres que no sean letras, numeros, guiones bajos o guiones medios

        if not sanitizedText:#Si el texto queda vacío después de sanitizar, tiramos un error de valor
            raise ValueError("El nombre de usuario no puede estar compuesto por caracteres inválidos.")

        return sanitizedText
    
    def checkEqPwd(self, pwd1, pwd2): #check Equal Passwords

        if pwd1 == pwd2:
            return
        else:
            raise ValueError("Las passwords no coinciden") # le tiramos un error de valores
        
    def prepareAndStorePwd(self,username,pwd):
        codedPwd = pwd.encode('utf-8')
        hashedPwd = bcrypt.hashpw(codedPwd, bcrypt.gensalt())
        self.dataHelper.addUser(username, hashedPwd.decode('utf-8'))#la password se tiene que pasar codificada en utf-8 para q json permita su serializacion

    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dataHelper.getUser(username) 
        if hashedpwd is None:
            raise ValueError("Usuario inexistente")#No esta bueno darle tanta informacion a un posible atacante, entonces mejor poner invalido
        if bcrypt.checkpw(pwd.encode('utf-8'), hashedpwd.encode('utf-8')):
            return "OK"
        else:
            raise ValueError("Password Incorrecto")
    
