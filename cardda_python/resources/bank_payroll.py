from cardda_python.resources.base_resource import BaseResource


class BankPayroll(BaseResource):
    name = 'bank_payrolls'
    nested_objects = {
        "sender": "BankAccount",
        "bank_transactions": "BankTransaction"
    }