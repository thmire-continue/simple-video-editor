from pymemcache.client.base import Client

class StorageManager():
    def __init__(self):
        self.__storage = None
        
    def __del__(self):
        self.__storage.close()

    def init_storage(self):
        self.__storage = Client(('localhost', 11211))

    def set(self, key, value):
        self.__storage.set(key, value)

    def get(self, key):
        return self.__storage.get(key)

storage_manager = StorageManager()
