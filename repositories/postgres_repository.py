import psycopg

from pathlib import Path

from .base import LedgerRepository

from account import Account
from transaction import Transaction, TransactionType

from datetime import datetime

class PostgresRepository(LedgerRepository):
    def __init__(
            self, 
            dbname: str, 
            user: str,
            password: str = "",
            host: str = "",
            port: int = 5432
        ) -> None:

        self._db = psycopg.connect(
            dbname=dbname, 
            user=user,
            password = password,
            host=host,
            port=port,
        )
        crs = self._db.cursor()

        schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema_postgres.sql"
        with open(schema_path) as file:
            schema = file.read()
            crs.execute(schema)

        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def _row_to_account(self, row: tuple) -> Account:
        """
        row[0] - id\n
        row[1] - owner\n
        row[2] - balance\n
        """

        return Account(
            row[0],
            row[1],
            row[2]
        )

    def _row_to_transaction(self, row: tuple) -> Transaction:
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
            row[5]
        )

    def create_account(self, owner, balance = 0) -> Account:
        crs = self._db.cursor()

        if not owner.strip():
            raise ValueError("Owner should be non empty")
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        
        crs.execute("insert into accounts(owner, balance) values(%s, %s) returning *", (owner, balance))
        row = crs.fetchone()

        self._db.commit()

        return self._row_to_account(row)

    def get_account(self, account_id) -> Account:
        crs = self._db.cursor()
        crs.execute("select * from accounts where id = %s", (account_id,))
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
            "update accounts set owner = %s, balance = %s where id = %s",
            (account.owner, account.balance, account.id)
        )

        self._db.commit()

    def create_transaction(
        self, 
        amount, 
        transaction_type, 
        from_account_id, 
        to_account_id
    ):
        crs = self._db.cursor()
        crs.execute(
            "insert into transactions(type, amount, from_account_id, to_account_id) values(%s, %s, %s, %s) returning *",
            (transaction_type.value, amount, from_account_id, to_account_id)
        )

        row = crs.fetchone()

        self._db.commit()

        transaction = self._row_to_transaction(row)

        return transaction


    def get_transactions(self):
        crs = self._db.cursor()
        crs.execute("select * from transactions")

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = self._row_to_transaction(row)

            transactions.append(transaction)

        return transactions

    def get_account_transactions(self, account_id):
        crs = self._db.cursor()
        crs.execute("select * from transactions where from_account_id = %s or to_account_id = %s", (account_id, account_id))

        rows = crs.fetchall()

        transactions = []

        for row in rows:
            transaction = self._row_to_transaction(row)

            transactions.append(transaction)

        return transactions