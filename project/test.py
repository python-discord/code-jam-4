#! /usr/bin/python3

from tkinter import *                                                                                                   

cal = Tk()                                                                                                              
cal.title("Calculator")                                                                                                 
operator=""                                                                                                             
text_Input =StringVar()                                                                                                 



btn1=Button(cal,  text=("1"), padx=16, bd=8, font=('arial',20,'bold'),  fg="purple").grid(row=1,column=0)                                                                                                                                      
cal.mainloop()   
