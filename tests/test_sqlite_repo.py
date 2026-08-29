from datetime import datetime
from sqlite3 import connect

import pytest

from ledger import Ledger
from repositories.sqlite_repository import SQLiteRepository
from transaction import TransactionType


def test_data_saves_in_db(tmp_path):
    repo1 = SQLiteRepository(tmp_path / "test.db")
    ledger1 = Ledger(repo1)

    ledger1.create_account("user1", 200)

    repo1.close()

    repo2 = SQLiteRepository(tmp_path / "test.db")
    ledger2 = Ledger(repo2)

    account = ledger2.get_account(1)

    assert account.id == 1
    assert account.owner == "user1"
    assert account.balance == 200

    repo2.close()


def test_is_transaction_type_enum(tmp_path):
    repo = SQLiteRepository(tmp_path / "test.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.deposit(1, 1000)

    transaction = ledger.get_transactions()[0]
    assert isinstance(transaction.transaction_type, TransactionType)

    repo.close()


def test_is_created_at_datetime(tmp_path):
    repo = SQLiteRepository(tmp_path / "test.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.withdraw(1, 100)

    transaction = ledger.get_transactions()[0]
    assert isinstance(transaction.created_at, datetime)

    crs = connect(tmp_path / "test.db").cursor()

    created_at = crs.execute("select created_at from transactions limit 1").fetchone()[
        0
    ]
    assert isinstance(datetime.fromisoformat(created_at), datetime)

    repo.close()


def test_get_account_transactions(tmp_path):
    repo = SQLiteRepository(tmp_path / "test.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    ledger.withdraw(1, 100)

    transaction = ledger.get_account_transactions(1)[0]

    assert transaction.transaction_type == TransactionType.WITHDRAW

    repo.close()


def test_foreign_keys(tmp_path):
    repo = SQLiteRepository(tmp_path / "test.db")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 1000)

    ledger.transfer(1, 2, 500)

    crs = connect(tmp_path / "test.db").cursor()
    transaction = crs.execute("select * from transactions").fetchone()

    assert transaction[3] == ledger.get_account(1).id
    assert transaction[4] == ledger.get_account(2).id

    repo.close()


@pytest.fixture(scope="session")
def smth(tmp_path):
    repo = SQLiteRepository(tmp_path / "test.db")
    ledger = Ledger(repo)

    account = ledger.create_account("user1", 1000)

    assert account.id == 1
    assert account.owner == "user1"
    assert account.balance == 1000

    repo.close()
