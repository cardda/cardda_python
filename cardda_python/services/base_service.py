from typing import Any, Dict, List
from abc import ABC, abstractclassmethod
from cardda_python.http_client import HttpClient
from cardda_python.resources import BaseResource


class BaseService(ABC):
    def __init__(self, client: HttpClient) -> None:
        self._client = client.extend(
            base_url= f"{client.base_url}/{self.resource.name}"
        )
    
    def __getattr__(self, attr):
        if attr not in self.__class__.methods:
            raise AttributeError(
                f"{self.__class__.__name__} does not implement '{attr}'"
            )
        return getattr(self, f"_{attr}")

    @property
    @abstractclassmethod
    def resource() -> BaseResource:
        pass

    @property
    @abstractclassmethod
    def methods() -> List[str]:
        pass

    def _all(self, **params) -> List[BaseResource]:
        response = self._client.all(params)
        return [self.resource(data) for data in response]

    def _create(self, **data) -> BaseResource:
        response =  self._client.create(data)
        return self.resource(response)

    def _find(self, id: str) -> BaseResource:
        response = self._client.find(id)
        return self.resource(response)
    
    def _save(self, obj: BaseResource):
        response = self._client.update(obj.id, obj.as_json())
        return obj.overwrite(response)
    
    def _delete(self, obj: BaseResource):
        response = self._client.delete(obj.id)
        return self.resource(response)