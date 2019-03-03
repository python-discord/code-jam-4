
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
            "You misclicked, right? Of course you did.",
            "A task with no title? Seriously?",
            "Do you even have a task?",
            "Dude, tasks without a title?",
            "Wow, no goals? Or have you simply forgotten?",
            "Dang, never knew task titles were optional.."
        ]
        passive_agressive_descriptions = [
            "What?",
            "You can't even describe your task?",
            "Elaborate it somehow...",
            "Now, this is just plain lazy",
            "Not sure why you left this blank, hm?",
        ]
        passive_agressive_deadlines = [
            "I guess deadlines just aren't real to you",
            "So your task is probably just a dream",
            "You miss the deadlines just like how storm trooper misses Jedi",
            "Did you know that the ultimate inspiration is the deadline?",
            "Oh, I didn't know you don't like having deadlines.. Explains a lot",
            "Not saying you're unproductive, but...",
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
        self.file.write_file(self.data)
        self.tup = [tuple(d.values()) for d in self.data]
        return self.tup
