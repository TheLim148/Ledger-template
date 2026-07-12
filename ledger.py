from datetime import datetime

from account import Account
from transaction import Transaction, TransactionType
from operations import deposit, withdraw, transfer


class Ledger():
    def __init__(self) -> None:
        self.accounts: dict[int, Account] = {}
        self.transactions: list[Transaction] = []

        self._next_account_id = 1
        self._next_transaction_id = 1

    def create_account(self, owner: str, balance: int = 0) -> Account:
        account = Account(
            id = self._next_account_id,
            owner = owner,
            balance = balance,
        )

        self.accounts[account.id] = account
        self._next_account_id += 1

        return account

    def get_account(self, account_id: int) -> Account:
        try:
            return self.accounts[account_id]
        except KeyError:
            raise ValueError("Account not found")

    def deposit(self, account_id: int, amount: int) -> Transaction:
        account = self.get_account(account_id)

        deposit(account, amount)

        return self._add_transaction(
            type=TransactionType.DEPOSIT,
            amount=amount,
            from_account_id=None,
            to_account_id=account.id,
        )

    def withdraw(self, account_id: int, amount: int) -> Transaction:
        account = self.get_account(account_id)

        withdraw(account, amount)

        return self._add_transaction(
            type=TransactionType.WITHDRAW,
            amount=amount,
            from_account_id=account.id,
            to_account_id=None,
        )

    def transfer(
        self, 
        from_account_id: int, 
        to_account_id: int, 
        amount: int
    ) -> Transaction:
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        transfer(from_account, to_account, amount)

        return self._add_transaction(
            type=TransactionType.TRANSFER,
            amount=amount,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
        )
    
    def get_transactions(self) -> list[Transaction]:
        return self.transactions.copy()

    def get_account_transactions(self, account_id: int) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.from_account_id == account_id
            or transaction.to_account_id == account_id
        ]

    def _add_transaction(
        self,
        type: TransactionType,
        amount: int,
        from_account_id: int | None,
        to_account_id: int | None,
    ) -> Transaction:
        transaction = Transaction(
            id = self._next_transaction_id,
            type = type,
            amount = amount,
            from_account_id = from_account_id,
            to_account_id = to_account_id,
            created_at = datetime.now()
        )

        self.transactions.append(transaction)
        self._next_transaction_id += 1

        return transaction
