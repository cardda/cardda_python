from dotenv import load_dotenv
from workers.transactions_worker import TransactionsWorker


if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env

    worker = TransactionsWorker()
    worker.execute()





