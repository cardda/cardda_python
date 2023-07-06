from abc import ABC, abstractclassmethod
from typing import Any, Dict
from importlib import import_module


class BaseResource(ABC):
    allowed_nested_attributes = []
    nested_objects = {}

    def __init__(self, json_data: Dict[str, Any]) -> None:
        self._attributes = []
        self.inject_attributes(json_data)

    @property
    def ignored_attributes(self):
        return ["updated_at", "created_at"]
    
    @property
    @abstractclassmethod
    def name() -> str:
        pass

    def as_json(self):
        json_dict = { 
            k: getattr(self, k) for k in self._attributes 
                if k not in self.ignored_attributes and not self.is_nested_obj(k)
        }
        for k in self._attributes:
            if k not in self.ignored_attributes and k in self.allowed_nested_attributes:
                value = getattr(self, k)
                json_dict[k] = value.as_json() if issubclass(type(value), BaseResource) else value
        return json_dict
    
    def is_nested_obj(self, key) -> bool:
        try:
            value = getattr(self, key)
        except AttributeError:
            value = None
        if type(value) in [int, str, bool] or (
            value == None and key in self._attributes):
            return False
        return True

    def inject_attributes(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, self.objectize(key, value))
            self._attributes.append(key)
        
    def overwrite(self, json_data):
        for attr in self._attributes:
            delattr(self, attr)
        self._attributes = []
        self.inject_attributes(json_data)
        return self
    
    def objectize(self, key: str, value: Any):
        if key in self.nested_objects.keys() and value:
            module = import_module("cardda_python.resources")
            klass = getattr(module, self.nested_objects[key])
            print(klass)
            print(value)
            if isinstance(value, list):
                return [klass(item) for item in value]
            else:
                return klass(value) 
        else:
            return value