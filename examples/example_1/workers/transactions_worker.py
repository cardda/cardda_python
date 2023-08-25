from models import WireTransfer
from .base_worker import BaseWorker
import os
from httpx import HTTPStatusError
import json
import time

class TransitionPendingException(Exception):
        def __init__(self, message="Cardda entity detected with a transition different from null"):
            super().__init__(message)

class TransactionsWorker(BaseWorker):
    TRANSACTION_INVALID_STATUS = "NON_VALID"
    TRANSACTION_ENROLLED_STATUS = "enqueued"
    RECIPIENT_ENROLLED_STATUS = "approved"

    def __init__(self) -> None:
        super().__init__()
        self.recipients_service = self.cardda_client.banking.recipients
        self.transactions_service = self.cardda_client.banking.transactions
        self.bank_key_id = os.environ.get("CARDDA_BANK_KEY_ID", "key_id")
        self.bank_account_id = os.environ.get("CARDDA_BANK_ACCOUNT_ID", "account_id")
        self._transactions = []
        self._recipients = []
        self.transactions_metadata = {}
        self.recipients_metadata = {}
    
    @property
    def transactions(self):
        return self._transactions

    @property
    def recipients(self):
        return self._recipients

    @transactions.setter
    def transactions(self, new_transactions):
        self._transactions = new_transactions
        self.transactions_metadata = {}
        # initialize metadata
        for tx in  self._transactions:
            self.transactions_metadata[tx] = {
                "cardda_id": None,
                "cardda_status": None,
                "recipient": None
            }
        # store unique recipients
        unique_recipients = { json.dumps(self.parse_recipient(db_tx)) for db_tx in self.transactions}
        self.recipients = list(map(lambda r: json.loads(r), unique_recipients))

    @recipients.setter
    def recipients(self, new_recipients):
        self._recipients = new_recipients
        self.recipients_metadata = {}
        # initialize metadata
        for idx, rec in enumerate(self._recipients):
            self.recipients_metadata[idx] = {
                "cardda_id": None,
                "cardda_status": None
            }
            # link rec to tx
            for tx in self.transactions_of_recipient(rec):
                self.transactions_metadata[tx]["recipient"] = rec
    
    def execute(self, attempts=10, wait_for=20):
        """
        Handles the amount of attemts to enqueue the transactions, and the waiting time bewteen them (for cardda async transitions).
        At the end will report the successfuly enrolled transactions.
        """
        remaining_attempts = attempts
        while remaining_attempts > 0:
            try:
                self.main_task()
            except TransitionPendingException:
                time.sleep(wait_for)
                remaining_attempts -= 1
            finally:
                self.iteration_report()
    
    def main_task(self):
        """
        high level description of the tasks to be completed
        """
        self.load_transactions()

        # enroll recipients
        should_wait_for_transitions = False
        for recipient in self.recipients:
            try:
                enrolled_recipient = self.validate_recipient(recipient)
                if not enrolled_recipient: self.enroll_recipient(recipient)
            except TransitionPendingException:
                should_wait_for_transitions = True

        if should_wait_for_transitions: raise TransitionPendingException()
       
        # enroll transactions
        for db_tx in self.transactions:
            try:
                enrolled_transaction = self.validate_transaction(db_tx)
                if not enrolled_transaction: self.enroll_transaction(db_tx)
            except TransitionPendingException:
                should_wait_for_transitions = True
        if should_wait_for_transitions: raise TransitionPendingException()
        
    def load_transactions(self):
        """
        Fetch transactions to be created from the db
        """
        with self.get_session() as session:
            self.transactions = session.query(WireTransfer).all()

    def validate_recipient(self, recipient):
        # to make it faster
        if self.recipients_metadata[self.recipients.index(recipient)]["cardda_status"] == self.RECIPIENT_ENROLLED_STATUS:  return True 

        # query cardda to check the recipient
        recipient_query = {
            "owner_id": self.bank_account_id,
            **recipient
        }
        response = self.recipients_service.all(**recipient_query)
        if len(response) > 0:
            # store metadata
            recipient_match = response[0]
            self.recipients_metadata[self.recipients.index(recipient)]["cardda_id"] = recipient_match.id
            self.recipients_metadata[self.recipients.index(recipient)]["cardda_status"] = recipient_match.status
            # check status and transitions
            if recipient_match.transition:
                raise TransitionPendingException()
            elif recipient_match.status == self.RECIPIENT_ENROLLED_STATUS:
                return True
        return False
    
    def enroll_recipient(self, recipient):
        if self.recipients_metadata[self.recipients.index(recipient)]["cardda_id"]:
            # enroll if draft
            cardda_recipient = self.recipients_service.find(self.recipients_metadata[self.recipients.index(recipient)]["cardda_id"])
            enroll_query = {
                    "owner_id":self.bank_account_id,
                    "bank_key_id":self.bank_key_id,
                }
            self.recipients_service.enroll(cardda_recipient, **enroll_query)
        else:
            # create if doesnt exists
            recipient_payload = {
                "alias": recipient["name"], # you could do something more fancy here
                "bank_key_id": self.bank_key_id,
                **recipient
            }
            self.recipients_service.create(**recipient_payload)
            raise TransitionPendingException()

    def validate_transaction(self, db_tx):
        if self.transactions_metadata[db_tx]["cardda_status"] == self.TRANSACTION_ENROLLED_STATUS: return True
    

        if self.transactions_metadata[db_tx]["cardda_id"]:
            cardda_tx = self.transactions_service.find(self.transactions_metadata[db_tx]["transaction_id"])
            self.transactions_metadata[db_tx]["cardda_id"] = cardda_tx.id
            self.transactions_metadata[db_tx]["cardda_status"] = cardda_tx.status
            if cardda_tx.transaction:
                raise TransitionPendingException()
            elif cardda_tx.status == self.TRANSACTION_ENROLLED_STATUS:
                return True
        return False

    def enroll_transaction(self, db_tx):
        if self.transactions_metadata[db_tx]["cardda_status"] == self.TRANSACTION_INVALID_STATUS: return


        if self.transactions_metadata[db_tx]["cardda_id"]:
            cardda_tx = self.transactions_service.find(self.transactions_metadata[db_tx]["transaction_id"])
            enqueue_query = { "bank_key_id": self.bank_key_id }
            self.transactions_service.enqueue(cardda_tx, **enqueue_query)
        else:
            transaction = self.parse_transaction(db_tx)
            transaction_payload = {
                "bank_payroll_id": None,
                "bank_key_id": self.bank_key_id,
                **transaction
            }
            try:
                cardda_tx = self.transactions_service.create(**transaction_payload)
                self.transactions_metadata[db_tx]["cardda_id"] = cardda_tx.id
                self.transactions_metadata[db_tx]["cardda_status"] = cardda_tx.status
            except HTTPStatusError as exc:
                if exc.response.status_code == 400:
                    self.transactions_metadata[db_tx]["status"] = self.TRANSACTION_INVALID_STATUS
                else:
                    print(exc)

    def iteration_report(self):
        """
        Group transactions by their last known status, and log that info in the console
        """
        report = "Attempt finished, this are the transactions statuses at the end:\n"
        statuses = {}
        for tx in self.transactions:
            metadata = self.transactions_metadata[tx]
            if metadata["cardda_status"] not in statuses.keys():
                statuses[metadata["cardda_status"]] = []
            
            statuses[metadata["cardda_status"]].append(tx.__repr__())
        for status, txs in statuses.items():
            report += f"{status}:\n" + "\n".join(txs)
        print(report)

    def parse_transaction(self, tx):
        """
        construct a bank transaction hash from the transaction
        """
        recipient = self.transactions_metadata[tx]["recipient"]
        return {
            "description": tx.commentary,
            "amount": tx.amount,
            "sender_id": self.bank_account_id,
            "recipient_id": self.recipients_metadata[self.recipients.index(recipient)]["cardda_id"]
        }

    def parse_recipient(self, tx):
        """
        construct a bank recipient hash from the transaction
        """
        return {
            "rut": tx.rut,
            "email": tx.email,
            "name": f"{tx.name} {tx.lastname}",
            "account_number": tx.account_number,
            "account_type": self.parse_account_type(tx.account_type),
            "bank_id": self.parse_bank(tx.account_bank)
        }
        
    def parse_bank(self, bank_str):
        """
        parse the internal company bank names to the cardda bank_ids
        """
        return bank_str

    def parse_account_type(self, account_type_str):
        """
        parse the internal company bank account types to the cardda account_types
        """
        return account_type_str

    def transactions_of_recipient(self, recipient):
        return [db_tx for db_tx in self.transactions if json.dumps(self.parse_recipient(db_tx)) == json.dumps(recipient)]