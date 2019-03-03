import pickle
import sqlite3
import sys

import qdarkstyle
from PySide2.QtSql import QSqlDatabase
from PySide2.QtWidgets import QApplication

from project.widgets import CreatePassword, MainWindow

DB_NAME = "library.sqlite"


def create_db():
    """Create the playlist's database file and table if they don't exist.

    The created database should be accessed using :meth:`PySide2.QtSql.QSqlDatabase.database`, the
    name being specified via :const:`project.library.DB_NAME`.

    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            create table if not exists playlist (
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


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Music Player")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    create_db()

    try:
        password = pickle.load(open("mycatfellonmykeyboard.omigosh", "rb"))
    except FileNotFoundError:
        create_password = CreatePassword()
        create_password.display()
        password = create_password.new_password
        pickle.dump(password, open("mycatfellonmykeyboard.omigosh", "wb"))

    window = MainWindow(password)
    window.setWindowTitle("Music Player")
    window.show()

    sys.exit(app.exec_())
