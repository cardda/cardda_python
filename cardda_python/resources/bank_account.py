from cardda_python.resources.base_resource import BaseResource

class BankAccount(BaseResource):
    name = 'bank_accounts'
    nested_objects = {
        "recipients": "BankRecipient",
        "bank_transactions": "BankTransaction",
        "bank_payrolls": "BankPayroll",
    }