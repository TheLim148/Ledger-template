import pytest

from model import Account
from operations import deposit, withdraw, transfer


def test_deposit_increase_balance():
    account = Account(1, "user1", 100)
    deposit(account, 200)
    assert account.balance == 300

def test_withdraw_decrease_balance():
    account = Account(2, "user2", 500)
    withdraw(account, 300)
    assert account.balance == 200

def test_transfer_updates_both_balances():
    account1 = Account(3, "user3", 1000)
    account2 = Account(4, "user4", 500)

    transfer(account1, account2, 500)
    assert account1.balance == 500
    assert account2.balance == 1000

def test_transfer_preserves_total_balance():
    account1 = Account(5, "user5", 100)
    account2 = Account(6, "user6", 400)

    total_before = account1.balance + account2.balance
    transfer(account1, account2, 50)
    total_after = account1.balance + account2.balance

    assert total_before == total_after


def test_transfer_to_same_account():
    account = Account(7, "user7", 1000)

    with pytest.raises(
        ValueError,
        match="Accounts should be different"
    ):
        transfer(account, account, 10)

def test_withdraw_amount_greater_than_balance():
    account = Account(8, "user8", 500)
    with pytest.raises(
        ValueError,
        match="Insufficient funds",
    ):
        withdraw(account, 1000)

def test_transfer_amount_greater_than_balance():
    account1 = Account(9, "user9", 500)
    account2 = Account(10, "user10", 1000)
    
    with pytest.raises(
        ValueError,
        match="Insufficient funds",
    ):
        transfer(account1, account2, 700)
 
    assert account1.balance == 500
    assert account2.balance == 1000

def test_withdraw_zero_amount():
    account = Account(11, "user11", 1000)
    with pytest.raises(ValueError):
        withdraw(account, 0)

    assert account.balance == 1000

def test_withdraw_negative_amount():
    account = Account(12, "user12", 1000)
    with pytest.raises(ValueError):
        withdraw(account, -100)

    assert account.balance == 1000

def test_deposit_zero_amount():
    account = Account(1, "user1", 1000)
    with pytest.raises(ValueError):
        deposit(account, 0)

def test_deposit_negative_amount():
    account = Account(2, "user2", 1000)
    with pytest.raises(ValueError):
        deposit(account, -500)

def test_create_account_with_bad_id():
    with pytest.raises(ValueError):
        Account(0, "user0", 100)

def test_create_account_with_bad_owner():
    with pytest.raises(ValueError):
        Account(15, "", 100)

def test_create_account_with_spaces_instead_of_owner():
    with pytest.raises(ValueError):
        Account(16, "   ", 100)

def test_create_account_with_bad_balance():
    with pytest.raises(ValueError):
        Account(17, "user17", -10)