import argparse

from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=""
    )

    parser.add_argument(
        "--storage", 
        choices=["memory", "sqlite"],
        default="sqlite",
        help="Storage backend to usage"
    )

    parser.add_argument(
        "--db-path", 
        type=Path,
        default=Path("./database.db"),
        help="Path to sqlite database file",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Seed demo data"
    )

    return parser