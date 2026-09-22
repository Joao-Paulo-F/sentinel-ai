import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "sentinel.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    DATABASE_DIR.mkdir(exist_ok=True)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection = get_connection()

    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Banco criado com sucesso em: {DATABASE_PATH}")