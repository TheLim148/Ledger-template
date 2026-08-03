from sqlite3 import connect
from pathlib import Path

with connect("database.db") as db:
    crs = db.cursor()
    with open(Path("./schema.sql")) as file:
        sql = file.read()
        crs.executescript(sql)


with connect("database.db") as db:
    crs = db.cursor()
    crs.execute("PRAGMA table_info('transactions');")

    tables = crs.fetchall()
    for table in tables:
        print(table)


    for account in crs.execute("select * from accounts"):
        print(account)