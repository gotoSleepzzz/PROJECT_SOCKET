import tkinter as tk
from tkinter import messagebox
import socket

HOST = "192.168.1.7"
PORT = 61113
server_address = (HOST,PORT)
LOGIN_CODE = '1'

class Login_Form():
    def __init__(self):
        self.role = -1
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.resizable(0,0)

        scrW = self.root.winfo_screenwidth()
        scrH = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d'%(scrW/4,scrH/3,scrW/2-scrW/8,scrH/2-scrH/5))

        tk.Label(self.root,text='Username').place(x=80,y=30)
        tk.Label(self.root,text='Password').place(x=80,y=60)

        self.name_input = tk.Entry(self.root, width=20, borderwidth=1)
        self.passw_input = tk.Entry(self.root, width=20, borderwidth=1, show='*')
        self.name_input.place(x=180,y=30)
        self.passw_input.place(x=180,y=60)

        self.login_btn = tk.Button(self.root,text='LOGIN',width=18, justify='center', border=1, command=self.login)
        self.register_btn = tk.Button(self.root,text='REGISTER',width = 18,justify='center', border=1, command=self.register)
        self.login_btn.place(x=180,y=120)
        self.register_btn.place(x=180,y=150)

    def login(self, event = None):
        username = self.name_input.get()
        password = self.passw_input.get()
        if username != "" and password != "":
            try:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(server_address)
                
                s.sendall(bytes(LOGIN_CODE,'utf8'))
                
                s.sendall(bytes(username,'utf8'))
                r = s.recv(100)
                s.sendall(bytes(password,'utf8'))
                respond = s.recv(100)
                flag = respond.decode('utf8')
                
                print(flag)
            finally:
                s.close()

            #No account
            if flag == '-1':
                tk.messagebox.showinfo("Show info","Account does not exist")
                self.role = -1
            #Client
            elif flag == '0':
                self.role = 0
                self.root.quit()
            #Admin
            else:
                self.role = 1
                self.root.quit()

    def Role(self):
        return self.role

    def register(self):
        pass

    def run(self):
        self.root.mainloop()