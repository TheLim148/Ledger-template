from PySide6.QtWidgets import QApplication

from gui.window import LedgerWindow
from repositories.in_memory_repository import InMemoryRepository
from repositories.sqlite_repository import SQLiteRepository
from ledger import Ledger
from parser import create_parser

import sys

def main():
    parser = create_parser()

    args = parser.parse_args()    

    if args.storage == "memory":
        repo = InMemoryRepository()
    elif args.storage == "sqlite":
        repo = SQLiteRepository(args.db_path)
    else:
        raise ValueError(f"Unknown storage: {args.storage}")
        
    ledger = Ledger(repository=repo)


    app = QApplication([])

    window = LedgerWindow(
        seed_demo=args.demo, 
        ledger=ledger
    )


    window.show()
    window.setFocus()

    app.exec()

    if hasattr(repo, "close"):
        repo.close()


if __name__ == "__main__":
    main()
