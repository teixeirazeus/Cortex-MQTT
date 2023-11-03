from abc import ABC, abstractmethod

class MemoryManager(ABC):

    @abstractmethod
    def store_short_term(self, data):
        pass

    @abstractmethod
    def store_long_term(self, key, data):
        pass

    @abstractmethod
    def retrieve_long_term(self, key):
        pass
