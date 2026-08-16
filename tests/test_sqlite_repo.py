from repositories.sqlite_repository import SQLiteRepository
from ledger import Ledger

from pathlib import Path

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
