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
from tkinter import Button, Tk, StringVar


class Num(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['bg'] = "pink"
        self['fg'] = "purple"


class Op(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['bg'] = "purple"
        self['fg'] = "pink"


cal = Tk()
cal.title("Calculator")
operator = ""
text_Input = StringVar()

# Number Buttons
btn1 = Num(cal, text=("1")).grid(row=1, column=0)
btn2 = Num(cal, text=("2")).grid(row=1, column=1)
btn3 = Num(cal, text=("3")).grid(row=1, column=2)
btn4 = Num(cal, text=("4")).grid(row=2, column=0)
btn5 = Num(cal, text=("5")).grid(row=2, column=1)
btn6 = Num(cal, text=("6")).grid(row=2, column=2)
btn7 = Num(cal, text=("7")).grid(row=3, column=0)
btn8 = Num(cal, text=("8")).grid(row=3, column=1)
btn9 = Num(cal, text=("9")).grid(row=3, column=2)
btn0 = Num(cal, text=("0")).grid(row=4, column=1)


# Operator buttons
op1 = Op(cal, text=("+")).grid(row=1, column=3)
op2 = Op(cal, text=("-")).grid(row=2, column=3)
op3 = Op(cal, text=("*")).grid(row=3, column=3)
op4 = Op(cal, text=("/")).grid(row=4, column=3)
op5 = Op(cal, text=("=")).grid(row=4, column=2)


cal.mainloop()
