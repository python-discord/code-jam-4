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
from tkinter import Button, Tk, StringVar, Frame
import tkinter as tk

class Num(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.val = int(self['text'])
        self['bg'] = "pink"
        self['fg'] = "purple"
        # command = add_num(self['text'])



class Op(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['bg'] = "purple"
        self['fg'] = "pink"
        # command = add_num(self['text'])

class Calculator(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        
        # Number Buttons
        self.btn1 = None
        self.btn2 = None
        self.btn3 = None
        self.btn4 = None
        self.btn5 = None
        self.btn6 = None
        self.btn7 = None
        self.btn8 = None
        self.btn9 = None
        self.btn0 = None
        
        # Operator buttons
        self.op1 = None
        self.op2 = None
        self.op3 = None
        self.op4 = None
        self.op5 = None
        
        self.create()
    
    def create(self):
        """
        Generates the actual GUI
        """
        self.btn1 = Num(self, text=("1"), command = self.add_num()).grid(row=1, column=0)
        self.btn2 = Num(self, text=("2")).grid(row=1, column=1)
        self.btn3 = Num(self, text=("3")).grid(row=1, column=1)
        self.btn4 = Num(self, text=("4")).grid(row=1, column=1)
        self.btn5 = Num(self, text=("5")).grid(row=1, column=1)
        self.btn6 = Num(self, text=("6")).grid(row=1, column=1)
        self.btn7 = Num(self, text=("7")).grid(row=1, column=1)
        self.btn8 = Num(self, text=("8")).grid(row=1, column=1)
        self.btn9 = Num(self, text=("9")).grid(row=1, column=1)
        self.btn0 = Num(self, text=("0")).grid(row=1, column=1)
        
        # Operator buttons
        self.op1 = Op(self, text=("+")).grid(row=1, column=3)
        self.op2 = Op(self, text=("-")).grid(row=2, column=3)
        self.op3 = Op(self, text=("*")).grid(row=3, column=3)
        self.op4 = Op(self, text=("/")).grid(row=4, column=3)
        self.op5 = Op(self, text=("=")).grid(row=4, column=2)
        
    def add_num(self):
        print(self['val'])









root = tk.Tk()
app = Calculator(master = root)
app.mainloop()
