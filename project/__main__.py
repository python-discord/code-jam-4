#! /usr/bin/python3

"""
A GUI calculator with built in obfuscation.
This application is built on tkinter. See the official
documentation and linked resources here:
    https://docs.python.org/3/library/tkinter.html

Requirements:
    Python 3.
"""
import tkinter as tk

class Calculator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.entry = None       #Where the entered operations go
        self.entry_label = None
        
        self.proc = None        #Displays processed operations
        self.proc_label = None
        
        self.answer  = None     #Answer line
        self.answer_label = None
        
        self.a = tk.StringVar() #String representation of self.entry
        self.b = tk.StringVar() #String representation of self.proc
        self.c = tk.StringVar() #String representation of self.answer
        self.c.set("0")

        self.create_form()     

    def create_form(self):
        """
        Create the gui,
        and buttons when called.
        """

        self.pilot_label = tk.Label(
            self,
            text="Pilot: ",
        )
        self.pilot = tk.Entry(
            self,
            width=30,
            textvariable = self.a,
        )
        self.pilot_label.pack(side="top")
        self.pilot.pack(side=tk.TOP)

        self.pwd_label = tk.Label(
            self,
            text="Password: ",
        )
        self.pwd = tk.Entry(
            self,
            show="*",
            width=30,
            textvariable = self.b
        )
        self.pwd_label.pack(side="top")
        self.pwd.pack(side=tk.TOP)         
        

        self.launch_button = tk.Button(
            self,
            text = self.launch_text.get(),
			bg = "teal",
			fg = "white",
            command=self.do_countdown,
        )
        
        self.launch_button.pack(side=tk.BOTTOM)

    def do_countdown(self):
        """
        When the user clicks the login button, this callback
        is invoked. Make it do a countdown. The first time
        it is clicked, the button text should change to "3".
        The next time to "2", then to "1", and then to "LIFTOFF!".

        If the username or the password are blank, this
        callback should not do anything.
        """
        
        if (self.a.get() != "") and (self.b.get() != ""):
            """
            Checks both Pilot & PWD are not empty
            """
            self.counter += 1
            if self.counter == 1:
                self.launch_button["text"] = "3"
            elif self.counter == 2:
                self.launch_button["text"] = "2"
            elif self.counter == 3:
                self.launch_button["text"] = "1"
            elif self.counter == 4:
                self.launch_button["text"] = "LIFTOFF!"    


root = tk.Tk()
app = RocketShipControlPanel(master=root)
app.mainloop()
 
