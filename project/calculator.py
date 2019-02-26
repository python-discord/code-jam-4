from tkinter import*

cal = Tk()
cal.title("Calculator")
operator=""
text_Input =StringVar()

def add_num(val):
    print(val)

txtDisplay = Entry(cal,font=('arial',20,'bold'), textvariable=text_Input, bd=30, insertwidth=4, bg="pink", justify='right').grid(columnspan=4)

btn1=Button(cal,  text=("1"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=1,column=0)
btn2=Button(cal,  text=("2"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=1,column=1)
btn3=Button(cal,  text=("3"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=1,column=2)
btn4=Button(cal,  text=("4"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=2,column=0) 
btn5=Button(cal,  text=("5"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=2,column=1) 
btn6=Button(cal,  text=("6"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=2,column=2)
btn7=Button(cal,  text=("7"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=3,column=0)
btn8=Button(cal,  text=("8"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=3,column=1) 
btn9=Button(cal,  text=("9"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=3,column=2)
btn0=Button(cal,  text=("0"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple", bg="pink").grid(row=4,column=1)

cal.mainloop()

