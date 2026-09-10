import os
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from errors import DatabaseError
from gui.window import LedgerWindow
from ledger import Ledger
from parser import create_parser
from repositories.in_memory_repository import InMemoryRepository
from repositories.postgres_repository import PostgresRepository
from repositories.sqlite_repository import SQLiteRepository


def main():
    parser = create_parser()

    args = parser.parse_args()

    app = QApplication([])

    try:
        if args.storage == "memory":
            repo = InMemoryRepository()
        elif args.storage == "sqlite":
            repo = SQLiteRepository(args.db_path)
        elif args.storage == "postgres":
            dbname = os.environ["POSTGRES_DB"]
            user = os.environ["POSTGRES_USER"]
            password = os.getenv("POSTGRES_PASSWORD", "")
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = int(os.getenv("POSTGRES_PORT", "5432"))

            repo = PostgresRepository(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
        else:
            raise ValueError(f"Unknown storage: {args.storage}")

        ledger = Ledger(repository=repo)

        window = LedgerWindow(seed_demo=args.demo, ledger=ledger)

    except DatabaseError:
        QMessageBox.warning(None, "Error", "Не удалось подключиться к базе данных")
        traceback.print_exc()
        return
    except Exception:
        traceback.print_exc()

    window.show()
    window.setFocus()

    app.exec()

    if hasattr(repo, "close"):
        repo.close()


if __name__ == "__main__":
    main()
