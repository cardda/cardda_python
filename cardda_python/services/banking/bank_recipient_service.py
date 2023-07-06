from cardda_python.services.base_service import BaseService
from cardda_python.resources import BankRecipient

class BankRecipientService(BaseService):
    resource = BankRecipient
    methods = ["all", "find", "save", "create"]

    def authorize(self, obj: BankRecipient, **data):
        response = self._client._request("POST", f"/{obj.id}/authorize", data=data)
        obj.overwrite(response)
        return obj
    
    def enroll(self, obj: BankRecipient, **data):
        response = self._client._request("POST", f"/{obj.id}/enroll", data=data)
        obj.overwrite(response)
        return obj