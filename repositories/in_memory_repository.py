from datetime import datetime

from account import Account
from transaction import Transaction

from .base import LedgerRepository

class InMemoryRepository(LedgerRepository):
    def __init__(self) -> None:
        
        self.accounts: dict[int, Account] = {}
        self.transactions: list[Transaction] = []

        self._next_account_id = 1
        self._next_transaction_id = 1

    def create_account(self, owner, balance = 0) -> Account:
        account = Account(
            id = self._next_account_id,
            owner = owner,
            balance = balance,
        )

        self.accounts[account.id] = account
        self._next_account_id += 1

        return account

    def get_account(self, account_id) -> Account:
        try:
            return self.accounts[account_id]
        except KeyError:
            raise ValueError("Account not found")

    def get_accounts(self) -> list[Account]:
        return list(self.accounts.values())

    def update_account(self, account) -> None:
        self.accounts[account.id] = account

    def get_transactions(self) -> list[Transaction]:
        return self.transactions.copy()

    def get_account_transactions(self, account_id) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.from_account_id == account_id
            or transaction.to_account_id == account_id
        ]

    def create_transaction(
        self,
        amount,
        transaction_type,
        from_account_id,
        to_account_id
    ) -> Transaction:
        transaction = Transaction(
            id = self._next_transaction_id,
            transaction_type=transaction_type,
            amount=amount,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            created_at=datetime.now()
        )

        self.transactions.append(transaction)
        self._next_transaction_id += 1

        return transaction
