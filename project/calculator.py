from tkinter import *

def btnClick(numbers) :
    global operator
    operator=operator + str(numbers)
    text_Input.set(operator)

def btnClearDisplay():
    global operator
    operator=""
    text_Input.set("")  

def btnEqualsInput():
    global operator
    sumup=str(eval(operator))
    text_Input.set(sumup)
    operator=""

cal = Tk()
cal.title("Calculator")
operator=""
text_Input =StringVar()

def add_num(val):
    print(val)

txtDisplay = Entry(cal,font=('arial',20,'bold'), textvariable=text_Input, bd=30, insertwidth=4, bg="pink", justify='right').grid(columnspan=4)

btn1=Button(cal,  text=("1"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(1)).grid(row=1,column=0)
btn2=Button(cal,  text=("2"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(2)).grid(row=1,column=1)
btn3=Button(cal,  text=("3"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(3)).grid(row=1,column=2)
btn4=Button(cal,  text=("4"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(4)).grid(row=2,column=0) 
btn5=Button(cal,  text=("5"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(5)).grid(row=2,column=1) 
btn6=Button(cal,  text=("6"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(6)).grid(row=2,column=2)
btn7=Button(cal,  text=("7"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(7)).grid(row=3,column=0)
btn8=Button(cal,  text=("8"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(8)).grid(row=3,column=1) 
btn9=Button(cal,  text=("9"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(9)).grid(row=3,column=2)
btn0=Button(cal,  text=("0"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(0)).grid(row=4,column=1)

btncle=Button(cal,  text=("C"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=btnClearDisplay).grid(row=4,column=0)

btnequ=Button(cal,  text=("="), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=btnEqualsInput).grid(row=5,column=3)

btnbra=Button(cal,  text=("("), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("(")).grid(row=5,column=0)
btnket=Button(cal,  text=(")"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(")")).grid(row=5,column=1)
btndec=Button(cal,  text=("."), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick(".")).grid(row=5,column=2)

btnpi = Button(cal, text="pie"),  padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("3")).grid(row=4,column=2) 

# space here for one more button maybe we should add pi you know like in case the user gets a bit hungry, this app may ultimately hate the users but we have to lure them in at the start with nice things maybe a nice cherry pi will do just fine

btnadd=Button(cal,  text=("+"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("+")).grid(row=1,column=3)
btnsub=Button(cal,  text=("-"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("-")).grid(row=2,column=3)
btnmul=Button(cal,  text=("*"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("*")).grid(row=3,column=3)
btndiv=Button(cal,  text=("/"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink", command=lambda:btnClick("/")).grid(row=4,column=3)



cal.mainloop()

