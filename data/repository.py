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

    @abstractmethod
    def save_symbols(self, symbols : list):
        pass

    @abstractmethod
    def load_symbols(self):
        pass

    @abstractmethod
    def get_symbols_updated_at(self):
        pass