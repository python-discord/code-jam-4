import tkinter as tk

class security_window(tk.Frame):

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.username_field = tk.Entry(self, width = 30)
        self.password_field = tk.Entry(self, width = 30, show = "*")
        self.username_field.place(x=70, y=10)
        self.password_field.place(x=70, y=40)
        self.submit_button = tk.Button(self, text = "Submit", background = "Green", command = self.submit)
        self.submit_button.place(x=70, y=60)
        self.text = tk.Label(self, text = """Username:
        
Password:""")
        self.text.place(x=10, y=10)

    def submit(self):
        username_entry = self.username_field.get()
        password_entry = self.password_field.get()
        if username_entry == 'squid' and password_entry == 'squid':
            self.password_field.delete(0,'end')
            self.username_field.delete(0,'end')
            self.password_confirm = self.username_field
            self.text['text'] = """Password:
            
Confirm:"""
            self.submit_button.config(command = self.new_password)

    def get_new_password(self):

        new_password = self.password_field.get()
        if new_password == self.password_confirm.get():
            self.new_password = new_password


security_root = tk.Tk()
security_root.geometry('280x85')
security_root.resizable(False,False)
app = security_window(security_root)
security_root.mainloop()