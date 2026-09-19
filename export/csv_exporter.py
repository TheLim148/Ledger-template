import csv
from datetime import datetime
from pathlib import Path

from account import Account
from transaction import Transaction


def _export_csv(data: list, path: Path, serializer):
    if not data:
        raise ValueError("Ошибка экспорта")

    first_row = serializer(data[0])
    fields = list(first_row.keys())

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for item in data:
            writer.writerow(serializer(item))


def _account_to_dict(account: Account) -> dict:
    return vars(account)


def _transaction_to_dict(transaction: Transaction) -> dict:
    data = vars(transaction).copy()
    data.update({"transaction_type": transaction.transaction_type.value})
    data.update({"created_at": datetime.isoformat(transaction.created_at)})

    return data


def export_accounts(accounts: list[Account], path: Path):
    _export_csv(accounts, path, _account_to_dict)


def export_transactions(transactions: list[Transaction], path: Path):
    _export_csv(transactions, path, _transaction_to_dict)
