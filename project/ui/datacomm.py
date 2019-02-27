import datetime
import time
from operator import itemgetter
import itertools
from .readWrite.rw import readWrite 

class datacomm:
    '''
    This class does the data communication and conversion between GUI and file
    '''

    #data refers to the data gotten from the Json file
    def __init__(self):
        self.rw = readWrite()
        self.data = rw.readInput()#get from Json Read
        self.pass_to_GUI() #This will pass to the GUI the moment the class is called

    #This list of functions passes data to file
    #CALL THIS FUNCTION
    def get_from_GUI(self, d):
        title = d['Title'] # Title will be in string
        desc = d['Description'] #Description is in string
        deadline = d['Deadline'] #Deadline is in int
        deleted = d['Deleted'] #This is in boolean

        #This function checks if it suppose to be added to or removed from data
        if (deleted == True):
            self.data[:] = [d for d in self.data if ((d.get('Title') != title) and (d.get('Description') != desc))]
        else:
            header = ('Title', 'Description', 'Deadline')
            converted_dt = self.unix_to_datetime(int(d['Deadline']))
            if (converted_dt):
                values = (i[0], i[1], converted_dt)
                d = dict(zip(header,values))
                self.data.append(d)
            else:
                return False #This means that Unix timing is before the actual current time which is impossible
            
        #Then Return to Json File
        #Call write to Json file
        self.rw = writeFile(self.data)
        #Get back to GUI
        return self.pass_to_GUI()

    '''
    This converts the unix in seconds to the current time(UTC) "Str format"
    '''
    def unix_to_datetime(self, dt):
        now = int(time.time())
        if ( dt - now <0):
            print("False")
            return False
        return str(datetime.datetime.utcfromtimestamp(dt))
    
    #This set of functions passes data to GUI
    '''
    This changes the data of list of dictionaries to tuple
    '''
    def pass_to_GUI(self):
        if is_empty(self.data):
            return []
        #self.header = ['Task Title', 'Task Desc', 'Date and Time', 'Mark']
        tup = [tuple(d.values()) for d in self.data]
        sorted(tup,key=itemgetter(2)) #This sorts the tup by date and time
        return tup
