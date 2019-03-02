
import datetime
from .read_write.rw import ReadWrite
from random import choice, randint


class DataComm:
    def __init__(self):
        self.file = ReadWrite()
        self.data = self.file.read_input()
        self.header = ('Title', 'Description', 'Deadline', 'Completed')
        self.update()

    # Takes a random task and deletes it
    def delete_task(self):
        if self.data:
            self.data.pop(randint(0, len(self.data) - 1))
        self.update()

    # Adds in a new task
    def add_task(self, d):
        task = dict()
        passive_agressive_titles = [
            "A task with no title? Seriously?",
            "Do you even have a task?",
            "Dude, tasks without a title?"
        ]
        passive_agressive_descriptions = [
            "What?",
            "You can't even describe your task?",
            "Elaborate it somehow...",
            "Now, this is just plain lazy"
        ]
        passive_agressive_deadlines = [
            "I guess deadlines just aren't real to you",
            "So your task is probably just a dream",
            "You miss the deadlines just like how storm trooper misses Jedi",
            "Did you know that the ultimate inspiration is the deadline?"
        ]
        task["Title"] = d.get("Title", choice(passive_agressive_titles))
        task["Description"] = d.get("Description", choice(
            passive_agressive_descriptions))
        task["Deadline"] = d.get(
            "Deadline", choice(passive_agressive_deadlines))
        if isinstance(task["Deadline"], int):
            task['Deadline'] = str(
                datetime.datetime.utcfromtimestamp(int(task['Deadline']))
            )
        task['Completed'] = False
        self.data.append(task)
        self.update()

    def update(self, table_model=None):
        # Writes to file
        self.file.write_file(self.data)
        self.tup = [tuple(d.values()) for d in self.data]
        return self.tup
        # I didn't sort it by date and time anymore since the passive_aggressive_statements are added in
