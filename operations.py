from account import Account


def deposit(account: Account, amount: int):
    _validate_amount(amount)
    account.balance += amount


def pprint(account: Account):
    print(
        f"ID:      {account.id}\nOWNER:   {account.owner}\nBALANCE: {account.balance}\n"
    )


def withdraw(account: Account, amount: int):
    _validate_amount(amount)

    if account.balance < amount:
        raise ValueError("Insufficient funds")

    account.balance -= amount


def transfer(src: Account, dst: Account, amount: int):
    _validate_amount(amount)

    if src.id == dst.id:
        raise ValueError("Accounts should be different")

    withdraw(src, amount)
    deposit(dst, amount)


def _validate_amount(amount: int) -> None:
    if amount is None:
        raise ValueError("Amount is empty")

    if amount <= 0:
        raise ValueError("Amount should be greater than 0")
