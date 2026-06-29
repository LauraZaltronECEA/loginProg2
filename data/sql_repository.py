import os
from sqlobject import SQLObject, StringCol, sqlhub, connectionForURI
from data.repository import Repository


class User(SQLObject):
    username = StringCol(unique=True, length=50)
    hashed_pwd = StringCol(length=255)


class Account(SQLObject):
    username = StringCol(length=50)
    currency = StringCol(length=3)
    balance = StringCol(length=50)


class SQLRepository(Repository):

    def __init__(self):
        db_dir = os.path.join(os.path.dirname(__file__), 'database')
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'database.sqlite')
        db_uri = 'sqlite:///' + db_path.replace('\\', '/')

        sqlhub.processConnection = connectionForURI(db_uri)
        User.createTable(ifNotExists=True)
        Account.createTable(ifNotExists=True)

    def add_user(self, username, hashed_pwd):
        User(username=username, hashed_pwd=hashed_pwd)

    def get_user(self, username):
        user = User.selectBy(username=username).getOne(None)
        return user.hashed_pwd if user else None

    def load_user_accounts(self, username):
        accounts = Account.selectBy(username=username)
        return {acc.currency: acc.balance for acc in accounts}

    def save_user_accounts(self, username, data):
        for acc in Account.selectBy(username=username):
            acc.destroySelf()
        for currency, balance in data.items():
            Account(username=username, currency=currency, balance=str(balance))
        return True
