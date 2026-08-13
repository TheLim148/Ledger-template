import pytest

from repositories.sqlite_repository import SQLiteRepository
from ledger import Ledger


def test_create_account():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    account = ledger.get_account(1)
    
    assert account.id == 1
    assert account.balance == 1000
    assert account.owner == "user1"

def test_account_not_found():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    with pytest.raises(
        ValueError,
        match="Account not found"
    ):
        account = ledger.get_account(1)

def test_get_accounts():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 1000)
    ledger.create_account("user3", 1000)

    accounts = ledger.get_accounts()

    assert len(accounts) == 3
    
def test_empty_get_accounts():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    accounts = ledger.get_accounts()

    assert accounts == []

def test_update_account():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)

    account_before = ledger.get_account(1)
    assert account_before.id == 1
    assert account_before.balance == 1000
    assert account_before.owner == "user1"

    ledger.deposit(1, 100)

    account_after = ledger.get_account(1)
    assert account_after.id == 1
    assert account_after.balance == 1100
    assert account_after.owner == "user1"

def test_1():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    trs1 = ledger.deposit(1, 100)
    trs1 = ledger.deposit(1, 100)

    trs2 = ledger.get_transactions()

    print(trs2)

def test_2():
    repo = SQLiteRepository(":memory:")
    ledger = Ledger(repo)

    ledger.create_account("user1", 1000)
    trs1 = ledger.deposit(1, 100)
    trs1 = ledger.deposit(1, 100)

    trs = ledger.get_account_transactions(1)
    print(trs)