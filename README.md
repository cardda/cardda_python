# Cardda Python Client Library

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/cardda/cardda-python.svg)](https://github.com/cardda/cardda-python/graphs/contributors)

**Cardda Python Client Library provides a simple way to interact with the Cardda API using Python.**

Version 1.0.0 of this library provides support for managing banking-related entities in the Cardda system.

## Installation

You can install the Cardda Python Client Library using pip:

```bash
pip install cardda-python
```

Certainly! Here's an example of a well-documented README in Markdown format explaining the usage of the library:

## Getting Started

To get started with the Cardda Python Library, you'll need an API key provided by Cardda. Once you have the API key, you can initialize the `CarddaClient` class:

```python
from cardda_python import CarddaClient

api_key = "YOUR_API_KEY"
client = CarddaClient(api_key)
```

The `CarddaClient` class is the entry point for interacting with the Cardda API. It requires your API key as a parameter.

## Banking Operations

The `CarddaClient` provides access to various banking operations through its `banking` property. You can access different banking services from this property:

```python
# Accessing the Bank Account Service
accounts_service = client.banking.accounts

# Accessing the Bank Recipient Service
recipients_service = client.banking.recipients

# Accessing the Bank Transaction Service
transactions_service = client.banking.transactions

# Accessing the Bank Payroll Service
payrolls_service = client.banking.payrolls

# Accessing the Bank Key Service
keys_service = client.banking.keys
```

Each service provides methods for performing operations on the corresponding resource.

## Example Usage

Here's an example of how you can use the Cardda Python Library to perform banking operations:

```python
# Retrieve all bank accounts
all_accounts = accounts_service.all()

# Create a new bank key
new_key_data = {
    # read our docs to find what you need to send
}
new_key = keys_service.create(**new_account_data)

# Find a specific bank transaction by ID
transaction_id = "TRANSACTION_ID"
transaction = transactions_service.find(transaction_id)

# Update a bank account
new_amount = 20000
transaction.amount = new_amount
accounts_service.save(transaction) # this operation is inplace but also returns the same obj

# Delete a bank account
account_id = "ACCOUNT_ID"
account = accounts_service.find(account_id)
deleted_account = accounts_service.delete(account)
```

You can use similar methods and operations for other banking resources like recipients, transactions, payrolls, accounts, and keys.

For more details on the available methods and operations check the property `Service.methods` of each service, since not all of them implement each basic operation among `["all", "find", "create", "save", "delete"]`.

## Custom Banking Services
This section provides examples of how to use each individual method for the respective service, showcasing the additional functionalities they offer beyond the standard CRUD operations.

### BankTransactionService

- `enqueue(obj, **data)`: Enqueues the specified bank transaction by sending a POST request to the API endpoint `/transactions/{id}/enqueue` with the given data. It updates the attributes of the object inplace and also returns the modified object.

- `dequeue(obj, **data)`: Dequeues the specified bank transaction by sending a PATCH request to the API endpoint `/transactions/{id}/dequeue` with the given data. Analog to enqueue

Example usage:
```python
transaction = BankTransaction(...)
enqueue_data = {...}  # Additional data for enqueuing
transaction_service.enqueue(transaction, **enqueue_data)

dequeue_data = {...}  # Additional data for dequeuing
transaction_service.dequeue(transaction, **dequeue_data)
```

### BankRecipientService

- `authorize(obj, **data)`: Authorizes the specified bank recipient by sending a POST request to the API endpoint `/recipients/{id}/authorize` with the given data. It updates the recipient object with the response data and returns the modified object.

- `enroll(obj, **data)`: Enrolls the specified bank recipient by sending a POST request to the API endpoint `/recipients/{id}/enroll` with the given data. It updates the recipient object with the response data and returns the modified object.

Example usage:
```python
recipient = BankRecipient(...)

enroll_data = {...}  # Additional data for enrollment
recipient_service.enroll(recipient, **enroll_data)

authorize_data = {...}  # Additional data for authorization
recipient_service.authorize(recipient, **authorize_data)
```

### BankPayrollService

- `enroll(obj, **data)`: Enrolls the specified bank payroll by sending a POST request to the API endpoint `/payrolls/{id}/enroll` with the given data. It updates the payroll object with the response data and returns the modified object.

- `remove(obj, **data)`: Removes the specified bank payroll by sending a PATCH request to the API endpoint `/payrolls/{id}/remove` with the given data. It updates the payroll object with the response data and returns the modified object.

- `authorize(obj, **data)`: Authorizes the specified bank payroll by sending a POST request to the API endpoint `/payrolls/{id}/authorize` with the given data. It updates the payroll object with the response data and returns the modified object.

- `preauthorize(obj, **data)`: Preauthorizes the specified bank payroll by sending a POST request to the API endpoint `/payrolls/{id}/preauthorize` with the given data. It updates the payroll object with the response data and returns the modified object.

- `validate_recipients(obj, **data)`: Validates the recipients of the specified bank payroll by sending a POST request to the API endpoint `/payrolls/{id}/validate_recipients` with the given data. It updates the payroll object with the response data and returns the modified object.

- `sync(obj, **data)`: Synchronizes the specified bank payroll by sending a POST request to the API endpoint `/payrolls/{id}/sync` with the given data. It updates the payroll object with the response data and returns the modified object.

Sync request don't update synchronously, they make sync request between the service and the bank to retrieve updated data you have to use the all() of the find() methods after the sync task was completed

Example usage:
```python
payroll = BankPayroll(...)
enroll_data = {...}  # Additional data for enrollment
payroll_service.enroll(payroll, **enroll_data)

other_payroll = BankPayroll(...)
payroll_service.remove(other_payroll)

validate_data = {...}  # Additional data for recipient validation
payroll_service.validate_recipients(payroll, **validate_data)

payroll_service.preauthorize(payroll)

authorize_data = {...}  # Additional data for authorization
payroll_service.authorize(payroll, **authorize_data)

payroll_service.sync(payroll, **sync_data)
```

### BankAccountService

- `preauthorize_transactions(obj, **data)`: Preauthorizes transactions for the specified bank account by sending a POST request to the API endpoint `/accounts/{id}/preauthorize` with the given data. It returns a list of BankTransaction objects representing the preauthorized transactions.

- `authorize_transactions(obj, **data)`: Authorizes transactions for the specified bank account by sending a POST request to the API endpoint `/accounts/{id}/authorize` with the given data.

- `preauthorize_recipients(obj, **data)`: Preauthorizes recipients for the specified bank account by sending a POST request to the API endpoint `/accounts/{id}/preauthorize_recipients` with the given data. It returns a list of BankRecipient objects representing the preauthorized recipients.

- `authorize_recipients(obj, **data)`: Authorizes recipients for the specified bank account by sending a POST request to the API endpoint `/accounts/{id}/authorize_recipients` with the given data.

- `dequeue_transactions(obj, **data)`: Dequeues transactions for the specified bank account by sending a POST request to the API endpoint `/accounts/{id}/dequeue` with the given data. It returns the modified bank account object.

- `sync_transactions(obj, **data)`: Synchronizes transactions for the specified bank account by sending a PATCH request to the API endpoint `/accounts/{id}/sync_transactions` with the given data.

- `sync_recipients(obj, **data)`: Synchronizes recipients for the specified bank account by sending a PATCH request to the API endpoint `/accounts/{id}/
sync_recipients` with the given data.

- `sync_payrolls(obj, **data)`: Synchronizes payrolls for the specified bank account by sending a PATCH request to the API endpoint `/accounts/{id}/sync_payrolls` with the given data.


Example usage:
```python
account = BankAccount(...)
preauthorized_transactions = account_service.preauthorize_transactions(account, **preauthorize_data)

preauthorize_data = {...}  # Additional data for recipient preauthorization
preauthorized_recipients = account_service.preauthorize_recipients(account, **preauthorize_data)

account_service.authorize_recipients(account, **authorize_data)

authorize_data = {...}  # Additional data for transaction authorization
account_service.authorize_transactions(account, **authorize_data)

authordequeue_data = {...}  # Additional data for transaction dequeueing
account_service.dequeue_transactions(account, **dequeue_data)

# sync requests
sync_query = {...} # read our API docs to check what is required to be sent in the query
account_service.sync_transactions(account, from_date="10-02-2000" ...) # only as an example named param
account_service.sync_recipients(account, **sync_data)
account_service.sync_payrolls(account, **sync_data)

```

## License

The Cardda Python Library is licensed under the MIT License. See the LICENSE file for more information.