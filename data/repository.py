from abc import ABC, abstractmethod

class Repository(ABC):

    @abstractmethod
    def add_user(self, username, hashed_pwd):
        pass

    @abstractmethod
    def get_user(self, username):
        pass

    @abstractmethod
    def load_user_accounts(self, username):
        pass

    @abstractmethod
    def save_user_accounts(self, username, data):
        pass
