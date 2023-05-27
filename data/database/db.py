import sqlite3


ABSOLUTE_PATH = "/Users/torgerbocianowski/Desktop/Projects/pelagi/"
DATA_PATH = ABSOLUTE_PATH + "data/"
DATABASE_PATH = DATA_PATH + "database/"

def news_columns() -> dict:
    return {
        "id": "INTEGER PRIMARY KEY",
        "headline": "TEXT NOT NULL",
        "description": "TEXT NOT NULL",
        "sentiment": "VARCHAR(10)",
        "confidence": "REAL"
    }

def connect(db: str) -> sqlite3.Connection:
    if db.endswith(".db"):
        db = db[:-3]
    return sqlite3.connect(DATABASE_PATH + db.lower() + ".db")

def create_table(db: str, columns: dict = None) -> str:
    if db.endswith(".db"):
        db = db[:-3]
    if db == "news":
        columns = news_columns()
    query = f"CREATE TABLE IF NOT EXISTS {db} ("
    for column, data_type in columns.items():
        query += f"{column} {data_type}, "
    query = query[:-2] + ")"
    return query

def drop_table(db: str) -> str:
    conn = connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE {db}")
        conn.commit()
        print(f"Dropped table {db}")
    except Exception as e:
        print("Could not drop table")
        print(e)
    finally:
        conn.close()

def insert_data(db: str, columns: dict = None) -> str:
    if db.endswith(".db"):
        db = db[:-3]
    if db == "news":
        columns = news_columns()
    columns.pop("id")
    query = f"INSERT INTO {db} ("
    for column in columns.keys():
        query += f"{column}, "
    query = query[:-2] + ") VALUES ("
    for _ in columns.keys():
        query += "?, "
    query = query[:-2] + ")"
    return query

def write_to_db(db: str, data: tuple, columns: dict = None) -> None:
    conn = connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute(create_table(db, columns))
        cursor.execute(insert_data(db, columns), data)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Data already exists in database")
    finally:
        conn.close()

def query_db(db: str, query: str) -> list:
    conn = connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print("Could not query database")
        print(e)
    finally:
        conn.close()

    return results
