from cardda_python.services.base_service import BaseService
from cardda_python.resources import BankTransaction

class BankTransactionService(BaseService):
    resource = BankTransaction
    methods = ["all", "find", "save", "create"]

    def enqueue(self, obj: BankTransaction, **data):
        obj.raw_data = self._client._request("POST", f"/{obj.id}/enqueue", data=data)
        return self

    def dequeue(self, obj: BankTransaction, **data):
        obj.raw_data = self._client._request("PATCH", f"/{obj.id}/dequeue", data=data)
        return obj