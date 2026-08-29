from datetime import datetime
from pathlib import Path
from sqlite3 import connect

from account import Account
from transaction import Transaction, TransactionType

from .base import LedgerRepository


class SQLiteRepository(LedgerRepository):
    def __init__(self, path_to_db: Path) -> None:
        self._db = connect(path_to_db)
        crs = self._db.cursor()

        schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"
        with open(schema_path) as file:
            sql = file.read()
            crs.executescript(sql)

    def close(self) -> None:
        self._db.close()

    def _row_to_account(self, row: tuple):
        """
        row[0] - id\n
        row[1] - owner\n
        row[2] - balance\n
        """

        return Account(row[0], row[1], row[2])

    def _row_to_transaction(self, row: tuple):
        """
        row[0] - id\n
        row[1] - TransactionType\n
        row[2] - amount\n
        row[3] - from_account_id\n
        row[4] - to_account_id\n
        row[5] - created_at\n
        """

        return Transaction(
            row[0],
            TransactionType(row[1]),
            row[2],
            row[3],
            row[4],
            datetime.fromisoformat(row[5]),
        )

    def create_account(self, owner, balance=0) -> Account:
        crs = self._db.cursor()

        if not owner.strip():
            raise ValueError("Owner should be non empty")
        if balance < 0:
            raise ValueError("Balance cannot be negative")

        crs.execute(
            "insert into accounts(owner, balance) values(?, ?) returning *",
            (owner, balance),
        )
        row = crs.fetchone()

        self._db.commit()

        return self._row_to_account(row)

    def get_account(self, account_id: int) -> Account:
        crs = self._db.cursor()
        crs.execute("select * from accounts where id = ?", (account_id,))
        row = crs.fetchone()

        if row is None:
            raise ValueError("Account not found")
        else:
            account = self._row_to_account(row)

        return account

    def get_accounts(self) -> list[Account]:
        crs = self._db.cursor()
        crs.execute("select * from accounts")

        rows = crs.fetchall()

        accounts = []

        for row in rows:
            account = self._row_to_account(row)
            accounts.append(account)

        return accounts

    def update_account(self, account: Account) -> None:
        crs = self._db.cursor()
        crs.execute(
            "update accounts set owner = ?, balance = ? where id = ?",
            (account.owner, account.balance, account.id),
        )

        self._db.commit()

    def create_transaction(
        self, amount, transaction_type, from_account_id, to_account_id
    ) -> Transaction:
        created_at = datetime.now()

        crs = self._db.cursor()
        crs.execute(
            """
            insert into transactions(
                type, 
                amount, 
                from_account_id, 
                to_account_id, 
                created_at
            ) 
            values(?, ?, ?, ?, ?) returning *
            """,
            (
                transaction_type.value,
                amount,
                from_account_id,
                to_account_id,
                created_at.isoformat(),
            ),
        )
        row = crs.fetchone()

        self._db.commit()

        transaction = self._row_to_transaction(row)

        return transaction

    def get_transactions(self) -> list[Transaction]:
        crs = self._db.cursor()
        crs.execute("select * from transactions")

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = self._row_to_transaction(row)

            transactions.append(transaction)

        return transactions

    def get_account_transactions(self, account_id) -> list[Transaction]:
        crs = self._db.cursor()
        crs.execute(
            "select * from transactions where from_account_id = ? or to_account_id = ?",
            (account_id, account_id),
        )

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = self._row_to_transaction(row)

            transactions.append(transaction)

        return transactions
