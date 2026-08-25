from PySide6.QtWidgets import QApplication

from gui.window import LedgerWindow
from repositories.in_memory_repository import InMemoryRepository
from repositories.sqlite_repository import SQLiteRepository
from ledger import Ledger

import sys

def main():
    args = sys.argv[1:]
    seed_demo = False

    if "--demo" in args:
        seed_demo = True
    else:
        seed_demo = False

    repository = SQLiteRepository("./database.db")
    ledger = Ledger(repository=repository)


    app = QApplication([])
    window = LedgerWindow(seed_demo=seed_demo, ledger=ledger)


    window.show()
    window.setFocus()

    app.exec()
    repository.close()


if __name__ == "__main__":
    main()
