class LoggedUser:
    _instance = None

    def __new__(cls, username):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, username):
        if self._initialized:
            return
        self.username = username
        self._initialized = True

    def get_username(self):
        return self.username
