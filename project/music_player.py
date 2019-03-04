import sqlite3
import sys

import qdarkstyle
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QApplication, QDialog

from project.widgets import CreatePassword, MainWindow, PasswordPrompt

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
        cursor.execute("""
            create table if not exists credentials (
                id       integer primary key,
                password text
            );
        """)  # The lack of security is a feature ;)
        conn.commit()

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(DB_NAME)

    # TODO: Handle possible errors if db fails to open


def create_password() -> str:
    """Prompt for a password to be created and return it."""
    dialogue = CreatePassword()
    dialogue.exec_()

    if dialogue.result() != QDialog.Accepted:
        sys.exit()

    password = dialogue.new_password

    # upsert
    query = QSqlQuery(QSqlDatabase.database())
    query.prepare("""
            insert into credentials (id, password)
            values (0, :password)
            on conflict (id)
            do update set password=:password
        """)
    query.bindValue(":password", password)
    query.exec_()
    query.finish()

    return password


def get_password() -> str:
    """Return the password from the database."""
    query = QSqlQuery(QSqlDatabase.database())
    query.exec_("select password from credentials")

    if query.next():
        password = query.value(0)
        query.finish()
        return password


def login() -> str:
    """Prompt for the password and return it. Create one if one doesn't exist."""
    password = get_password()
    if password:
        prompt = PasswordPrompt(password)
        prompt.exec_()
        if prompt.result() != QDialog.Accepted:
            sys.exit(1)
    else:
        password = create_password()

    return password


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Music Player")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    create_db()
    password = login()

    window = MainWindow(password)
    window.setWindowTitle("Music Player")
    window.show()

    sys.exit(app.exec_())
