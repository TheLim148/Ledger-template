from dataclasses import dataclass


@dataclass
class Account:
    id: int
    owner: str
    balance: int

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("ID should be greater than 0")
        if not self.owner.strip():
            raise ValueError("Owner should be non empty")
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")
