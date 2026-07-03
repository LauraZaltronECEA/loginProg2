import json
import os
from datetime import datetime
from data.repository import Repository


class JsonRepository(Repository):

    def __init__(self):
        self.users_file = './data/users/users.json'
        self.symbols_file = './data/symbols/symbols.json'

    def add_user(self, username, hashed_pwd):
        users = self._deserialize(self.users_file)
        users[username] = hashed_pwd
        self._serialize(users, self.users_file)

    def get_user(self, username):
        users = self._deserialize(self.users_file)
        return users.get(username)

    def load_user_accounts(self, username):
        try:
            path = f'./data/userAcc/{username}.json'
            return self._deserialize(path)
        except FileNotFoundError:
            return {}

    def save_user_accounts(self, username, data):
        path = f'./data/userAcc/{username}.json'
        self._serialize(data, path)
        return True

    def save_symbols(self, symbols):
        data = {"updated_at": datetime.now().isoformat(), "symbols": symbols}
        os.makedirs(os.path.dirname(self.symbols_file), exist_ok=True)
        self._serialize(data, self.symbols_file)
        return True

    def load_symbols(self):
        try:
            data = self._deserialize(self.symbols_file)
            return data.get("symbols")
        except FileNotFoundError:
            return None

    def get_symbols_updated_at(self):
        try:
            data = self._deserialize(self.symbols_file)
            ts = data.get("updated_at")
            return datetime.fromisoformat(ts) if ts else None
        except FileNotFoundError:
            return None

    def _serialize(self, data, file):
        with open(file, "w") as f:
            f.write(json.dumps(data, indent=4))

    def _deserialize(self, file):
        with open(file, "r") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)

