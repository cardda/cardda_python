from cardda_python.services.base_service import BaseService
from cardda_python.resources import BankPayroll

class BankPayrollService(BaseService):
    resource = BankPayroll
    methods = ["all", "find", "save", "create", "delete"]

    def enroll(self, obj: BankPayroll, **data):
        response = self._client._request("POST", f"/{obj.id}/enroll", data=data)
        obj.overwrite(response)
        return obj

    def remove(self, obj: BankPayroll, **data):
        response = self._client._request("PATCH", f"/{obj.id}/remove", data=data)
        obj.overwrite(response)
        return obj
    
    def authorize(self, obj: BankPayroll, **data):
        response = self._client._request("POST", f"/{obj.id}/authorize", data=data)
        obj.overwrite(response)
        return obj
        
    def preauthorize(self, obj: BankPayroll, **data):
        response = self._client._request("POST", f"/{obj.id}/preauthorize", data=data)
        obj.overwrite(response)
        return obj
    
    def validate_recipients(self, obj: BankPayroll, **data):
        response = self._client._request("POST", f"/{obj.id}/validate_recipients", data=data)
        obj.overwrite(response)
        return obj  
    
    def sync(self, obj: BankPayroll, **data):
        response = self._client._request("POST", f"/{obj.id}/sync", data=data)
        obj.overwrite(response)
        return obj