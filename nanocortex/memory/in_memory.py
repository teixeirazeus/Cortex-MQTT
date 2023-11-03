import queue
from memory_manager import MemoryManager

class InMemoryManager(MemoryManager):

    def __init__(self):
        self.short_term_memory = queue.Queue()
        self.long_term_memory = {}

    def store_short_term(self, data):
        self.short_term_memory.put(data)

    def store_long_term(self, key, data):
        self.long_term_memory[key] = data

    def retrieve_long_term(self, key):
        return self.long_term_memory.get(key)