from sqlite3 import connect
from pathlib import Path

from .base import LedgerRepository

from account import Account
from transaction import Transaction, TransactionType

from datetime import datetime

class SQLiteRepository(LedgerRepository):
    def __init__(self, path_to_db: Path) -> None:
        self._db = connect(path_to_db)
        crs = self._db.cursor()
        with open(Path("./schema.sql")) as file:
            sql = file.read()
            crs.executescript(sql)

    def close(self) -> None:
        self._db.close()

    def create_account(self, owner, balance = 0) -> None:
        crs = self._db.cursor()

        if not owner.strip():
            raise ValueError("Owner should be non empty")
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        
        crs.execute("insert into accounts(owner, balance) values(?, ?)", (owner, balance))
        self._db.commit()

    def get_account(self, account_id: int) -> Account:
        crs = self._db.cursor()
        crs.execute("select * from accounts where id = ?", (account_id,))
        row = crs.fetchone()

        if row is None:
            raise ValueError("Account not found")
        else:
            account = Account(row[0], row[1], row[2]) 

        return account

    def get_accounts(self):
        crs = self._db.cursor()
        crs.execute("select * from accounts")

        rows = crs.fetchall()

        accounts = []

        for row in rows:
            account = Account(row[0], row[1], row[2])
            accounts.append(account)

        return accounts
        

    def update_account(self, account: Account) -> None:
        crs = self._db.cursor()
        crs.execute(
            "update accounts set owner = ?, balance = ? where id = ?", 
            (account.owner, account.balance, account.id)
        )

        self._db.commit()

    def create_transaction(
        self, 
        amount, 
        transaction_type, 
        from_account_id, 
        to_account_id
    ) -> Transaction:
        created_at = datetime.now()

        crs = self._db.cursor()
        crs.execute(
            "insert into transactions(type, amount, from_account_id, to_account_id, created_at) values(?, ?, ?, ?, ?) returning *",
            (transaction_type.value, amount, from_account_id, to_account_id, created_at.isoformat())
        )
        row = crs.fetchone()

        self._db.commit()

        transaction = Transaction(
            row[0], 
            TransactionType(row[1]), 
            row[2], 
            row[3], 
            row[4], 
            datetime.fromisoformat(row[5])
        )

        return transaction

    def get_transactions(self) -> list[Transaction]:
        crs = self._db.cursor()
        crs.execute("select * from transactions")

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = Transaction(
                row[0], 
                TransactionType(row[1]), 
                row[2], 
                row[3], 
                row[4], 
                datetime.fromisoformat(row[5])
            )
            transactions.append(transaction)

        return transactions

    def get_account_transactions(self, account_id) -> list[Transaction]:
        crs = self._db.cursor()
        crs.execute("select * from transactions where from_account_id = ? or to_account_id = ?", (account_id, account_id))

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = Transaction(
                row[0], 
                TransactionType(row[1]), 
                row[2], 
                row[3], 
                row[4], 
                datetime.fromisoformat(row[5])
            )
            transactions.append(transaction)

        return transactions
    