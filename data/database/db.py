import sqlite3
import os

from ..scraping.utils.helpers import get_sites

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

def news_columns() -> dict:
    return {
        "headline": "TEXT NOT NULL",
        "description": "TEXT NOT NULL",
        "sentiment": "VARCHAR(10)",
        "confidence": "REAL"
    }

def get_db_names(test=False) -> list[str]:
    sites = get_sites(test)
    db_names = []
    for site in sites:
        topics = sites[site]["topics"]
        for topic in topics:
            for subtopic in topics[topic]:
                try:
                    db_name = topics[topic][subtopic]["db_name"]
                    db_names.append(db_name)
                except KeyError:
                    print(topics[topic][subtopic])
                    continue
    return db_names

def connect(db: str) -> sqlite3.Connection:
    if db.endswith(".db"):
        db = db[:-3]
    return sqlite3.connect(ABSOLUTE_PATH + db.lower() + ".db")

def create_table(db: str, columns: dict = None, index_column: str = None) -> str:
    if db.endswith(".db"):
        db = db[:-3]
    if "news" in db.lower():
        columns = news_columns()
        # index_column = "headline"
    query = f"CREATE TABLE IF NOT EXISTS {db} (id INTEGER PRIMARY KEY, "
    for column, data_type in columns.items():
        query += f"{column} {data_type}, "
    query = query[:-2]
    query += "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
    
    if index_column:
        query += f";\nCREATE INDEX IF NOT EXISTS {index_column}_index ON {db} ({index_column})"
    
    return query


def insert_data(db: str, columns: dict = None) -> str:
    # check_headline = f" WHERE NOT EXISTS (SELECT 1 FROM {db} WHERE headline = {column['headline']})" if "news" in db.lower() else ""
    if db.endswith(".db"):
        db = db[:-3]
    query = f"INSERT INTO {db} ("
    for column in columns:
        query += f"{column}, "
    query = query[:-2] + ") SELECT "
    for _ in range(len(columns)):
        query += "?, "
    query = query[:-2] # + check_headline
    return query


def write_to_db(db: str, data: tuple, columns: dict = None, index_column: str = None) -> None:
    conn = connect(db)
    cursor = conn.cursor()

    if not columns and "news" in db.lower():
        columns = news_columns()

    try:
        create_table_query = create_table(db, columns, index_column)
        cursor.execute(create_table_query)
        conn.commit()
    except sqlite3.OperationalError:
        print("Table already exists: ", db)

    try:
        insert_data_query = insert_data(db, columns)
        cursor.execute(insert_data_query, data)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Data already exists in database: ", data)
    finally:
        conn.close()

def query_db(db: str, query: str) -> list:
    conn = connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise e
    finally:
        conn.close()

def drop_table(db: str) -> str:
    db = db.lower()
    conn = connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {db}")
        conn.commit()
        print(f"Dropped table {db}")
    except Exception as e:
        raise e
    finally:
        conn.close()

def drop_all_tables(test=False) -> None:
    db_names = get_db_names(test)
    if len(db_names) == 0:
        print("No tables to drop")
        return
    for db in db_names:
        drop_table(db)
    print("Dropped all tables")
