
import datetime
from .readWrite.rw import readWrite
from random import randint


class DataComm:
    def __init__(self):
        self.file = readWrite()
        self.data = self.file.readInput()
        self.header = ('Title', 'Description', 'Deadline', 'Completed')
        self.update()

    # Takes a random task and deletes it
    def delete_task(self):
        if not self.data:
            self.data.pop(randint(0, len(self.data)))
        self.update()

    # Adds in a new task
    def add_task(self, d):
        if "Description" not in d:
            passive_aggressive_statement = [
                "What?", "You can't even describe your task?", "Elaborate it somehow...", "Now, this is just plain lazy"
            ]
            d['Description'] = passive_aggressive_statement[randint(0, 3)]

        if "Deadline" not in d:
            passive_aggressive_statement = [
                "I guess deadlines just aren't real to you", "So your task is probably just a dream",
                "You miss the deadlines just like how storm trooper misses Jedi", "Did you know that the ultimate inspiration is the deadline?"
            ]
            d['Deadline'] = passive_aggressive_statement[randint(0, 3)]

        elif isinstance(d["Deadline"], int):
            d['Deadline'] = str(
                datetime.datetime.utcfromtimestamp(int(d['Deadline']))
            )

        d['Mark'] = False
        self.data.append(d)
        self.update()
        print(self.data)

    def update(self):
        # Writes to file
        self.file.writeFile(self.data)
        self.tup = [tuple(d.values()) for d in self.data]
        # I didn't sort it by date and time anymore since the passive_aggressive_statements are added in
