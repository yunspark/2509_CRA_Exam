class Singleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

a = Singleton.get_instance()
b = Singleton.get_instance()
print (a is b)