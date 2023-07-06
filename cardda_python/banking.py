from cardda_python.http_client import HttpClient
from cardda_python.services.banking import (
    BankTransactionService,
    BankRecipientService,
    BankPayrollService,
    BankKeyService,
    BankAccountService
)
from cardda_python.constants import BANKING_PREFIX

class BankingService:
    path_prefix = BANKING_PREFIX

    def __init__(self, client: HttpClient):
        self._client = client.extend(
            base_url= f"{client.base_url}/{self.path_prefix}"
        )
    
    @property
    def accounts(self):
        return BankAccountService(self._client)
    
    @property
    def recipients(self):
        return BankRecipientService(self._client)
    
    @property
    def transactions(self):
        return BankTransactionService(self._client)
    
    @property
    def payrolls(self):
        return BankPayrollService(self._client)
    
    @property
    def keys(self):
        return BankKeyService(self._client)