from datetime import datetime

from account import Account
from transaction import Transaction, TransactionType
from operations import deposit, withdraw, transfer

from repositories.base import LedgerRepository

class Ledger():
    def __init__(self, repository: LedgerRepository) -> None:

        self._repo = repository

    def create_account(self, owner: str, balance: int = 0) -> Account:
        return self._repo.create_account(owner, balance)

    def get_account(self, account_id: int) -> Account:
        return self._repo.get_account(account_id)

    def get_accounts(self) -> list[Account]:
        return self._repo.get_accounts()

    def deposit(self, account_id: int, amount: int) -> Transaction:
        account = self.get_account(account_id)

        deposit(account, amount)

        self._repo.update_account(account)

        transaction = self._repo.create_transaction(
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            from_account_id=None,
            to_account_id=account.id
        )

        return transaction

    def withdraw(self, account_id: int, amount: int) -> Transaction:
        account = self.get_account(account_id)

        withdraw(account, amount)

        self._repo.update_account(account)

        transaction = self._repo.create_transaction(
            amount=amount,
            transaction_type=TransactionType.WITHDRAW,
            from_account_id=account.id,
            to_account_id=None,
        )

        return transaction

    def transfer(
        self, 
        from_account_id: int, 
        to_account_id: int, 
        amount: int
    ) -> Transaction:
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        transfer(from_account, to_account, amount)

        self._repo.update_account(from_account)
        self._repo.update_account(to_account)

        transaction = self._repo.create_transaction(
            amount=amount,
            transaction_type=TransactionType.TRANSFER,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
        )

        return transaction

    
    def get_transactions(self) -> list[Transaction]:
        return self._repo.get_transactions()

    def get_account_transactions(self, account_id: int) -> list[Transaction]:
        return self._repo.get_account_transactions(account_id)