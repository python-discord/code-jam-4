"""Database handling for calandar application."""
import sqlite3


class DBHandler:
    """Database Handler Class."""

    def __init__(self):
        """Initialise the database connection.

        Arguments:
            None
        Returns:
            None
        """
        self.conn = sqlite3.connect("events.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(
                ID INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT,
                date TEXT,
                description TEXT)""")
        # self.populate()

    def fetchEvents(self):
        """Fetch event from the database."""
        self.cursor.execute("""SELECT * FROM events""")
        # Fetch rows
        rows = self.cursor.fetchall()
        return rows

    def addEvent(self, name, location, date, description):
        """Create a new event and add it to the database."""
        self.cursor.execute('''INSERT INTO users(name,location,
                                                 date,description)
                                                 VALUES(?,?,?)''', (name,
                                                                    location,
                                                                    date,
                                                                    description
                                                                    )
                            )
        self.db.commit()

    # TESTING - ONLY USED IN DEVELOPMENT. REMOVE UPON RELEASE!!!
    def populate(self):
        """Use to populate the database with sample data."""
        self.cursor.execute(""" INSERT INTO events
                                (name,location,
                                description,date)
                                VALUES(?,?,?,?)""", ("Meeting",
                                                     "Office on 4th street",
                                                     """Talk about upcoming
                                                     work events""",
                                                     "03/03/2020"))
        self.conn.commit()
