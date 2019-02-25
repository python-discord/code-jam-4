#! /usr/bin/python3

"""
A GUI calculator with built in obfuscation.
This application is built on tkinter. See the official
documentation and linked resources here:
    https://docs.python.org/3/library/tkinter.html

Requirements:
    Python 3
    tkinter
"""
import tkinter as tk

class Calculator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.entry = None       #Where the entered operations go
   
        self.proc_label = None  #Where the processed operations are displayed
        
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

        self.entry = tk.Entry(
            self,
            width=30,
            textvariable = self.a,
        )
        self.entry.pack(side=tk.TOP)
        
        self.proc_label = tk.Label(
            self,
            text ="",
        )
        self.proc_label.pack(side = "top")
                
        self.ans_label = tk.Label(
            self,
            text = "",
        )
        self.ans_label.pack(side = "top")      


root = tk.Tk()
app = Calculator(master=root)
app.mainloop()
 
