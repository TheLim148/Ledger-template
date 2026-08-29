from abc import ABC, abstractmethod

from account import Account
from transaction import Transaction, TransactionType


class LedgerRepository(ABC):
    @abstractmethod
    def create_account(
        self,
        owner: str,
        balance: int = 0,
    ) -> None:
        pass

    @abstractmethod
    def get_account(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> None:
        pass

    @abstractmethod
    def create_transaction(
        self,
        amount: int,
        transaction_type: TransactionType,
        from_account_id: int | None,
        to_account_id: int | None,
    ) -> Transaction:
        pass

    @abstractmethod
    def get_transactions(self) -> list[Transaction]:
        pass

    @abstractmethod
    def get_account_transactions(self, account_id: int) -> list[Transaction]:
        pass
