from cardda_python.resources.base_resource import BaseResource


class BankRecipient(BaseResource):
    name = 'bank_recipients'
    nested_objects = {
        "owner": "BankAccount",
        "transactions": "BankTransaction"
    }