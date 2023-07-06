import httpx
from typing import Any, Dict, List
import json


class HttpClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.__client = None
    
    def extend(
        self,
        base_url=None,
        api_key=None,
    ):
        return HttpClient(
            base_url=base_url or self.base_url,
            api_key=api_key or self.api_key,
        )
    
    @property
    def _client(self) -> httpx.Client:
        if self.__client is None:
            self.__client = httpx.Client(base_url=self.base_url, headers=self.headers)
        return self.__client

    @property
    def headers(self):
        return {
            "Authorization": f'Bearer {self.api_key}',
            "Content-Type": "application/json"
            }
    
    def _request(self, method: str, endpoint: str = "", data = {}, params = {}):
        response = self._client.request(method, endpoint, params=params, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def all(self, params) -> List[Any]:
        response = self._request('GET', params=params)
        return response

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request('POST', data=data)
        return response

    def find(self, resource_id: str) -> Dict[str, Any]:
        response = self._request('GET', endpoint=f'/{resource_id}')
        return response

    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request('PATCH', endpoint=f'/{resource_id}', data=data)
        return response
    
    def delete(self, resource_id: str) -> Dict[str, Any]:
        response = self._request('DELETE', endpoint=f'/{resource_id}')
        return response