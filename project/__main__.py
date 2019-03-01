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
from tkinter import Button, Entry, StringVar, Tk
import random
import math


def btnClick(numbers):
    global operator
    operator = operator + str(numbers)
    text_Input.set(operator)


def btnTau():
    global operator
    c = random.randint(0, 101)

    if c <= 20:
        k = math.pi
    elif c <= 80:
        k = 2*math.pi
    else:
        k = math.floor(c/100)

    operator = operator + str(k)
    text_Input.set(operator)


def btnClearDisplay():
    global operator
    operator = ""
    text_Input.set("")


def btnEqualsInput():
    global operator
    sumup = str(eval(operator))
    text_Input.set(sumup)
    # operator=""  # uncomment this line to stop carry-over operations


numbers = [x for x in range(10)]


def assign_num():
    index = random.randint(0, len(numbers)-1)
    num = numbers[index]
    if len(numbers) >= 2:
        numbers.pop(index)
    return num


cal = Tk()
cal.title("Calculator")
operator = ""
text_Input = StringVar()


txtDisplay = Entry(cal, font=('arial', 20, 'bold'), textvariable=text_Input,
                   bd=30, insertwidth=4, bg="pink",
                   justify='right').grid(columnspan=4)

a = assign_num()
b = assign_num()
c = assign_num()
d = assign_num()
e = assign_num()
f = assign_num()
g = assign_num()
h = assign_num()
i = assign_num()
j = assign_num()


btn1 = Button(cal,  text=(str(a)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(a)).grid(row=1, column=0)
btn2 = Button(cal,  text=(str(b)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(b)).grid(row=1, column=1)
btn3 = Button(cal,  text=(str(c)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(c)).grid(row=1, column=2)
btn4 = Button(cal,  text=(str(d)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(d)).grid(row=2, column=0)
btn5 = Button(cal,  text=(str(e)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(e)).grid(row=2, column=1)
btn6 = Button(cal,  text=(str(f)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(f)).grid(row=2, column=2)
btn7 = Button(cal,  text=(str(g)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(g)).grid(row=3, column=0)
btn8 = Button(cal,  text=(str(h)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(h)).grid(row=3, column=1)
btn9 = Button(cal,  text=(str(i)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(i)).grid(row=3, column=2)
btn0 = Button(cal,  text=(str(j)), padx=16, bd=8, font=('arial', 20, 'bold'),
              fg="purple", bg="pink",
              command=lambda: btnClick(j)).grid(row=4, column=1)

btncle = Button(cal,  text=("C"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=btnClearDisplay).grid(row=4, column=0)

btnequ = Button(cal,  text=("="), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=btnEqualsInput).grid(row=5, column=3)

btnbra = Button(cal,  text=("("), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick("(")).grid(row=5, column=0)
btnket = Button(cal,  text=(")"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick(")")).grid(row=5, column=1)
btndec = Button(cal,  text=("."), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick(".")).grid(row=5, column=2)

btntau = Button(cal,  text=("\u03C4"), padx=16, bd=8, font=('cambria', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnTau()).grid(row=4, column=2)

btnadd = Button(cal,  text=("+"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick("+")).grid(row=1, column=3)
btnsub = Button(cal,  text=("-"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick("-")).grid(row=2, column=3)
btnmul = Button(cal, text=("*"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick("*")).grid(row=3, column=3)
btndiv = Button(cal, text=("/"), padx=16, bd=8, font=('arial', 20, 'bold'),
                fg="purple", bg="pink",
                command=lambda: btnClick("/")).grid(row=4, column=3)


cal.mainloop()
