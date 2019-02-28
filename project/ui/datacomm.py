
import datetime
import time
from operator import itemgetter
import itertools
from readWrite.rw import readWrite
from random import randint


class datacomm:
    def __init__(self):
        self.file = readWrite()
        self.data = self.file.readInput()
        return self.update()
        
    #Takes a random task and deletes it
    def deletedtask(self):
        #Get the size of self.data
        if (len(self.data) == 0):
            return []
        
        self.data.pop(randint(0, len(self.data)))
        return self.update()
    
    #Adds in a new task
    def addtask(self, d):
        header = ('Title', 'Description', 'Deadline', 'Mark')
        if not(d['Description']):
            passive_aggressive_statement = ["What?", "You can't even describe your task?","Elaborate it somehow...", "Now, this is just plain lazy"]
            d['Description'] = passive_aggressive_statement[randint(0, 3)]
            
        if not(d['Deadline']):
            passive_aggressive_statement = ["I guess deadlines just aren't real to you", "So your task is probably just a dream","You miss the deadlines just like how storm trooper misses Jedi","Did you know that the ultimate inspiration is the deadline?"]
            d['Deadline'] = passive_aggressive_statement[randint(0, 3)]
            
        elif(type(d['Deadline']) == "int"):
            d['Deadline'] = str(datetime.datetime.utcfromtimestamp(int(d['Deadline'])))

        d['Mark'] = False
        values = (d['Title'], d['Description'], d['Deadline'], d['Mark'])
        d = dict(zip(header,values))
        self.data.append(d)
        return self.update()

    def update(self):
        #Writes to file
        self.file.writeFile(self.data)
        if not(self.data):
            return []
        tup = [tuple(d.values()) for d in self.data]
        #I didn't sort it by date and time anymore since the passive_aggressive_statements are added in
        return tup
