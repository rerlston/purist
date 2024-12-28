from typing import Dict

class ObjectTypeManager:
    def __init__(self):
        self._types: Dict[str, object] = {}

    def register(self, name_to_register, type_to_register: object):
        self._types[name_to_register] = type_to_register

    def exists(self, name):
        return name in self._types
