from pathlib import Path
import sqlite3


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database files
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "onboardiq.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

def get_connection():
    """
    Create and return a SQLite database connection.

    Foreign-key enforcement is enabled for the connection.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def initialize_database():
    """
    Create the SQLite database schema from schema.sql.
    """
    connection = get_connection()

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()

        connection.executescript(schema)
        connection.commit()

    finally:
        connection.close()


def get_table_names():
    """
    Return all user-created tables in the database.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        return [row[0] for row in cursor.fetchall()]

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    tables = get_table_names()

    print("Database initialized successfully.")
    print("Tables created:")

    for table in tables:
        print(f"- {table}")