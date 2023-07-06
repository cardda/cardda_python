from cardda_python.services.base_service import BaseService
from cardda_python.resources import BankAccount, BankTransaction, BankRecipient

class BankAccountService(BaseService):
    resource = BankAccount
    methods = ["all", "find"]

    def preauthorize_transactions(self, obj: BankAccount, **data):
        res = self._client._request("POST", f"/{obj.id}/preauthorize", data=data)
        try:
            return [ BankTransaction(data) for data in res ]
        except:
            return res
        
    def authorize_transactions(self, obj: BankAccount, **data):
        return self._client._request("POST", f"/{obj.id}/authorize", data=data)

    def preauthorize_recipients(self, obj: BankAccount, **data):
        res = self._client._request("POST", f"/{obj.id}/preauthorize_recipients", data=data)
        try:
            return [ BankRecipient(data) for data in res ]
        except:
            return res
    
    def authorize_recipients(self, obj: BankAccount, **data):
        res = self._client._request("POST", f"/{obj.id}/authorize_recipients", data=data)
        try:
            return [ BankRecipient(data) for data in res ]
        except:
            return res
    
    def dequeue_transactions(self, obj: BankAccount, **data):
        res = self._client._request("POST", f"/{obj.id}/dequeue", data=data)
        return obj
    
    def sync_transactions(self, obj: BankAccount, **data):
        return self._client._request("PATCH", f"/{obj.id}/sync_transactions", data=data)

    def sync_recipients(self, obj: BankAccount, **data):
        return self._client._request("PATCH", f"/{obj.id}/sync_recipients", data=data)
    
    def sync_payrolls(self, obj: BankAccount, **data):
        return self._client._request("PATCH", f"/{obj.id}/sync_payrolls", data=data)