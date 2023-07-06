from cardda_python.resources.base_resource import BaseResource


class BankTransaction(BaseResource):
    name = 'bank_transactions'
    nested_objects = {
        "sender": "BankAccount",
        "recipient": "BankRecipient",
        "payroll": "BankPayroll"
    }