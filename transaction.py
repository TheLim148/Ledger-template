from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


@dataclass(frozen=True)
class Transaction:
    id: int
    transaction_type: TransactionType
    amount: int
    from_account_id: int | None
    to_account_id: int | None
    created_at: datetime
