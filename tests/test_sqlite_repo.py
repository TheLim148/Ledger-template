from repositories.sqlite_repository import SQLiteRepository
from ledger import Ledger
from transaction import TransactionType

from datetime import datetime

from pathlib import Path

from sqlite3 import connect

import os

TMP_PATH = Path("/tmp/")

def test_data_saves_in_db():
    repo1 = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger1 = Ledger(repo1)

    ledger1.create_account("user1", 200)

    repo1.close()

    repo2 = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger2 = Ledger(repo2)

    account = ledger2.get_account(1)

    assert account.id == 1
    assert account.owner == "user1"
    assert account.balance == 200

    os.remove(TMP_PATH / "tmp.db")

def test_is_transaction_type_enum():
    repo = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.deposit(1, 1000)

    transaction = ledger.get_transactions()[0]
    assert isinstance(transaction.transaction_type, TransactionType)

    os.remove(TMP_PATH / "tmp.db")

def test_is_created_at_datetime():
    repo = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.withdraw(1, 100)

    transaction = ledger.get_transactions()[0]
    assert isinstance(transaction.created_at, datetime)

    crs = connect(TMP_PATH / "tmp.db").cursor()

    created_at = crs.execute("select created_at from transactions limit 1").fetchone()[0]
    assert isinstance(datetime.fromisoformat(created_at), datetime)

    os.remove(TMP_PATH / "tmp.db")

def test_get_account_transactions():
    repo = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.withdraw(1, 100)

    transaction = ledger.get_account_transactions(1)[0]

    assert transaction.transaction_type == TransactionType.WITHDRAW

    os.remove(TMP_PATH / "tmp.db")

def test_foreign_keys():
    repo = SQLiteRepository(TMP_PATH / "tmp.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 1000)

    ledger.transfer(1, 2, 500)

    crs = connect(TMP_PATH / "tmp.db").cursor()
    transaction = crs.execute("select * from transactions").fetchone()

    assert transaction[3] == ledger.get_account(1).id
    assert transaction[4] == ledger.get_account(2).id

    os.remove(TMP_PATH / "tmp.db")