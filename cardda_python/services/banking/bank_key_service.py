from cardda_python.services.base_service import BaseService
from cardda_python.resources import BankKey

class BankKeyService(BaseService):
    resource = BankKey
    methods = ["all", "find", "save", "create"]