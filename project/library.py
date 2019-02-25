import sqlite3

from PySide2.QtSql import QSqlDatabase

DB_NAME = "library.sqlite"


def create_db():
    """Create the library's database file and table if they don't exist.

    The created database should be accessed using :meth:`PySide2.QtSql.QSqlDatabase.database`, the
    name being specified via :const:`project.library.DB_NAME`.

    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            create table if not exists library (
                id     integer primary key,
                path   text    not null,
                crc32  integer not null,
                title  text,
                artist text,
                album  text,
                date   text,
                genre  text
            );
        """)
        conn.commit()

    db = QSqlDatabase.addDatabase("SQLITE")
    db.setDatabaseName(DB_NAME)

    # TODO: Handle possible errors if db fails to open
