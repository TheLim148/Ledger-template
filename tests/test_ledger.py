import pytest

from ledger import Ledger
from transaction import TransactionType

from repositories.in_memory_repository import InMemoryRepository
from repositories.sqlite_repository import SQLiteRepository
from repositories.postgres_repository import PostgresRepository

@pytest.fixture(params=["memory", "sqlite", "postgres"])
def ledger(request):
    if request.param == "memory":
        repo = InMemoryRepository()

    if request.param == "sqlite":
        repo = SQLiteRepository(":memory:")

    if request.param == "postgres":
        repo = PostgresRepository("ledger_test", "ledger_user")
        repo._db.cursor().execute("truncate table accounts, transactions restart identity cascade")
        repo._db.commit()

    yield Ledger(repo)

    if hasattr(repo, "close"):
        repo.close()


def test_successful_create_account(ledger: Ledger):
    ledger.create_account("user1", 1000)
    account = ledger.get_account(1)

    assert account.id == 1
    assert account.owner == "user1"
    assert account.balance == 1000

def test_create_account_with_bad_owner(ledger: Ledger):
    with pytest.raises(ValueError, match="Owner should be non empty"):
        ledger.create_account("", 1000)
    
    with pytest.raises(ValueError, match="Owner should be non empty"):
       ledger.create_account("   ", 1000)

    with pytest.raises(ValueError, match="Owner should be non empty"):
       ledger.create_account("\n\r\t", 1000)

def test_create_account_with_bad_balance(ledger: Ledger):
    with pytest.raises(ValueError, match="Balance cannot be negative"):
        ledger.create_account("user1", -1000)

def test_create_account_increase_id(ledger: Ledger):
    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 1000)
    ledger.create_account("user3", 1000)

    assert len(ledger.get_accounts()) == 3
 
    for i in range(1, len(ledger.get_accounts())):
        assert ledger.get_account(i).id == i

def test_deposit_increase_balance(ledger: Ledger):
    ledger.create_account("user1", 1000)
    ledger.deposit(1, 500)

    assert ledger.get_account(1).balance == 1500
    assert ledger.get_account_transactions(1)[0].amount == 500 
    assert ledger.get_account_transactions(1)[0].transaction_type == TransactionType.DEPOSIT

def test_deposit_with_bad_amount(ledger: Ledger):
    ledger.create_account("user1", 1000)

    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.deposit(1, 0)
    
    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.deposit(1, -1000)

    assert ledger.get_account_transactions(1) == []
    assert ledger.get_account(1).balance == 1000

def test_deposit_account_not_found(ledger: Ledger):
    with pytest.raises(ValueError, match="Account not found"):
        ledger.deposit(999, 1000)
    
    assert ledger.get_transactions() == []

def test_withdraw_decrease_balance(ledger: Ledger):
    ledger.create_account("user1", 1000)
    ledger.withdraw(1, 500)

    assert ledger.get_account(1).balance == 500
    assert ledger.get_account_transactions(1)[0].amount == 500
    assert ledger.get_account_transactions(1)[0].transaction_type == TransactionType.WITHDRAW

def test_withdraw_insufficient_funds(ledger: Ledger):
    ledger.create_account("user1", 1000)
    
    with pytest.raises(ValueError, match="Insufficient funds"):
        ledger.withdraw(1, 2000)

    assert ledger.get_account(1).balance == 1000
    assert ledger.get_transactions() == []

def test_withdraw_account_not_found(ledger: Ledger):
    with pytest.raises(ValueError, match="Account not found"):
        ledger.withdraw(999, 1000)
    
    assert ledger.get_transactions() == []

def test_withdraw_with_bad_amount(ledger: Ledger):
    ledger.create_account("user1", 1000)

    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.withdraw(1, 0)

    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.withdraw(1, -1000)

    assert ledger.get_account_transactions(1) == []
    assert ledger.get_account(1).balance == 1000

def test_transfer_preserve_balance(ledger: Ledger):
    ledger.create_account("user1", 2000)
    ledger.create_account("user2", 500)

    account1 = ledger.get_account(1)
    account2 = ledger.get_account(2)

    total_before = account1.balance + account2.balance
    ledger.transfer(account1.id, account2.id, 500)

    account1_after = ledger.get_account(1)
    account2_after = ledger.get_account(2)

    total_after = account1_after.balance + account2_after.balance

    assert account1_after.balance == 1500
    assert account2_after.balance == 1000

    assert total_before == total_after

    assert ledger.get_account_transactions(account1.id)[0].amount == 500
    assert ledger.get_account_transactions(account2.id)[0].amount == 500

    assert ledger.get_account_transactions(account1.id)[0].transaction_type == TransactionType.TRANSFER
    assert ledger.get_account_transactions(account2.id)[0].transaction_type == TransactionType.TRANSFER

    assert ledger.get_account_transactions(account1.id)[0].from_account_id == account1.id
    assert ledger.get_account_transactions(account2.id)[0].to_account_id == account2.id

    assert ledger.get_transactions().__len__() == 1

def test_transfer_insufficient_funds(ledger: Ledger):
    ledger.create_account("user1", 2000)
    ledger.create_account("user2", 500)

    account1 = ledger.get_account(1)
    account2 = ledger.get_account(2)

    with pytest.raises(ValueError, match="Insufficient funds"):
        ledger.transfer(account2.id, account1.id, 1000)
    
    assert account1.balance == 2000
    assert account2.balance == 500
    assert ledger.get_transactions() == []

def test_transfer_account_not_found(ledger: Ledger):
    with pytest.raises(ValueError, match="Account not found"):
        ledger.transfer(42, 999, 1000)
    
    assert ledger.get_transactions() == []

def test_transfer_with_bad_amount(ledger: Ledger):
    ledger.create_account("user1", 2000)
    ledger.create_account("user2", 500)

    account1 = ledger.get_account(1)
    account2 = ledger.get_account(2)

    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.transfer(account1.id, account2.id, 0)
    
    with pytest.raises(ValueError, match="Amount should be greater than 0"):
        ledger.transfer(account1.id, account2.id, -1000)

    assert account1.balance == 2000
    assert account2.balance == 500
    
    assert ledger.get_account_transactions(account1.id) == []
    assert ledger.get_account_transactions(account2.id) == []
    

def test_transfer_to_same_account(ledger: Ledger):
    ledger.create_account("user1", 2000)
    account = ledger.get_account(1)

    with pytest.raises(ValueError, match="Accounts should be different"):
        ledger.transfer(account.id, account.id, 1000)

    assert ledger.get_account_transactions(account.id) == []

    assert account.balance == 2000
    
def test_get_transactions(ledger: Ledger):
    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 2000)

    ledger.deposit(1, 500)
    ledger.withdraw(2, 400)
    ledger.transfer(2, 1, 200)

    transactions = ledger.get_transactions()
    
    assert len(transactions) == 3

    for i in range(len(transactions)):
        assert transactions[i].id == i + 1

    assert transactions[0].amount == 500
    assert transactions[1].amount == 400
    assert transactions[2].amount == 200

def test_get_account_transactions(ledger: Ledger):
    ledger.create_account("user1", 1000)
    ledger.create_account("user2", 2000)

    ledger.deposit(1, 500)
    ledger.withdraw(2, 400)
    ledger.transfer(2, 1, 200)

    transactions_account1 = ledger.get_account_transactions(1)
    transactions_account2 = ledger.get_account_transactions(2)

    assert len(transactions_account1) == 2
    assert len(transactions_account2) == 2

    assert transactions_account1[0].transaction_type == TransactionType.DEPOSIT
    assert transactions_account1[1].transaction_type == TransactionType.TRANSFER
    
    assert transactions_account2[0].transaction_type == TransactionType.WITHDRAW
    assert transactions_account2[1].transaction_type == TransactionType.TRANSFER