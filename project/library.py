import sqlite3
from typing import Any, Dict, Optional

from PySide2.QtSql import QSqlDatabase, QSqlQuery

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
                title  text,
                artist text,
                album  text,
                genre  text,
                date   text,
                crc32  integer not null,
                path   text    not null
            );
        """)
        conn.commit()

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(DB_NAME)

    # TODO: Handle possible errors if db fails to open

def add_media(metadata: Dict[str, Any]) -> Optional[int]:
    """Add media to the library database.

    Parameters
    ----------
    metadata: Dict[str, Any]
        The metadata of the media to add.

    Returns
    -------
    Optional[int]
        The ID of the added media. See :meth:`PySide2.QtSql.QSqlQuery.lastInsertId`.

    """
    query = QSqlQuery(QSqlDatabase.database())
    query.prepare("""
        insert into library (path, crc32, title, artist, album, date, genre)
        values (?, ?, ?, ?, ?, ?, ?)
    """)

    query.addBindValue(metadata["path"])
    query.addBindValue(metadata["crc32"])
    query.addBindValue(metadata.get("title"))
    query.addBindValue(metadata.get("artist"))
    query.addBindValue(metadata.get("album"))
    query.addBindValue(metadata.get("date"))
    query.addBindValue(metadata.get("genre"))

    query.exec_()

    return query.lastInsertId()
