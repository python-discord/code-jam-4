"""Database handling for calandar application."""
import sqlite3
import json
from tkinter import messagebox


class DBHandler:
    """Database Handler Class."""

    def __init__(self):
        """Initialise the database connection.

        Arguments:
            None
        Returns:
            None
        """
        self.conn = sqlite3.connect("app.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(
                ID INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT,
                date TEXT,
                description TEXT)""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                ID INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT)""")
        with open("utils/jsonMessage.json") as jsonMessages:
            self.jsonMessages = json.load(jsonMessages)
        # self.populate()

    def fetchEvents(self):
        """Fetch event from the database.

        Arguments:
            None
        Returns:
            None
        """
        self.cursor.execute("""SELECT * FROM events""")
        # Fetch rows
        rows = self.cursor.fetchall()
        return rows

    def addEvent(self, name, location, date, description):
        """Create a new event and add it to the database.

        Arguments:
            name - name of event
            location - location of event
            date - date of event
            description - description of event
        Returns:
            None
        """
        self.cursor.execute('''INSERT INTO events(name,location,
                                                 date,description)
                                                 VALUES(?,?,?,?)''', (name,
                                                                      location,
                                                                      date,
                                                                      description))
        self.conn.commit()

    def removeEvent(self, id):
        """Remove an event from the database.

        Arguments:
            ID - The ID of the event that is to be removed
        Returns:
            None
        """
        # Remove the event with the specified ID
        self.cursor.execute("DELETE FROM events WHERE id = ?", (id,))
        print(f"Deleted event with ID: {id}")
        self.conn.commit()

    def addUser(self, username, password):
        """
        Add a user to the database.

        Arguments:
            entryName - the name to be added,
            entryPassword - the password for the user
        Returns:
            None
        """
        self.cursor.execute('''INSERT INTO users(username,password)
                              VALUES(?,?)''', (username, password))
        self.conn.commit()

    def tryLogin(self, username, password):
        """Attempt user login.

        Arguments:
            username - user's username
            password - user's password
        Returns:
            None
        """
        if len(username) < 1 or len(password) < 1:
            messagebox.showerror("Error",
                                 self.jsonMessages['populateLogin']
                                 )
            return
        self.cursor.execute("""SELECT * FROM users WHERE username=? AND password=?""",
                            (username, password))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            addUserMB = messagebox.askyesno("No user found",
                                            self.jsonMessages['noUser'])
            # If they select 'yes' on the messagebox
            if addUserMB:
                self.addUser(username, password)
                messagebox.showinfo("Success",
                                    self.jsonMessages['userAdded'])
            return
        # LOG IN THE USER, MAYBE A METHOD IN MAIN APP

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
                                                     "12/02"))
        self.conn.commit()
