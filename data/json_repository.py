import json
from data.repository import Repository

class JsonRepository(Repository):

    def __init__(self):
        self.users_file = './data/users/users.json'

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

    def _serialize(self, data, file):
        with open(file, "w") as f:
            f.write(json.dumps(data, indent=4))

    def _deserialize(self, file):
        with open(file, "r") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
