from cardda_python.http_client import HttpClient
from cardda_python.banking import BankingService
from cardda_python.constants import API_BASE_URL, API_VERSION

class CarddaClient:
    def __init__(self, api_key, custom_url=None, custom_version=None):
        self._client = HttpClient(
            base_url=f"{custom_url or API_BASE_URL}/{custom_version or API_VERSION}",
            api_key=api_key
        )
    
    @property
    def banking(self):
        return BankingService(self._client)
    
    