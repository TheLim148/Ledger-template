from model import Account
from operations import deposit, withdraw, transfer, pprint

def main():
    account = Account(1, "huh", 10000)
    account1 = Account(2, "huh2", 5000)
    try:
        pprint(account)
        pprint(account1)
        transfer(account, account1, 5000)
        pprint(account)
        pprint(account1)
        account2 = Account(3, "1", 100)

    except ValueError as err:
        print(f"{err}")

if __name__ == "__main__":
    main()
