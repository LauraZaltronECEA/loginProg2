import json

class DataHelper:
    def __init__(self):
        self.usersFile = './data/users/users.json'

    def addUser(self,username,hashedPwd):
        users = self.deserialize(self.usersFile)
        users[username] = hashedPwd
        self.serialize(users,self.usersFile)

    def getUser(self,username):
        users = self.deserialize(self.usersFile)
        try:
            return users[username] 
        except KeyError:#si no existe, tira KeyError
            return None

    def serialize(self,data,file):
        with open(file,"w") as f:
            f.write(json.dumps(data,indent=4))

    def deserialize(self,file):
        with open(file,"r") as f:
            return json.loads(f.read())

    #Serializacion y deserializacion a cuentas de usuario
    def loadUserAccounts(self, username):
        try:
            path = f'./data/userAcc/{username}.json'
            return self.deserialize(path)
        except FileNotFoundError:
            return {}

    def saveUserAccounts(self, username, data):
        try:
            path = f'./data/userAcc/{username}.json'
            self.serialize(data, path)
            return True
        except Exception as e:
            print("Error: {}".format(e.args[0]))