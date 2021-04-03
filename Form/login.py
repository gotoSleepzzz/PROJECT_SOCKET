import tkinter as tk
from tkinter import messagebox
import socket

LOGIN_CODE = '1'
REGISTER_CODE = '2'

class Register_Form():
    def __init__(self,user_socket):
        self.flag_exit = False  #to check window close
        self.root = tk.Toplevel()
        self.user_socket = user_socket
        self.root.title("REGISTER")
        self.root.resizable(0,0)

        scrW = self.root.winfo_screenwidth()
        scrH = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d'%(scrW/4,scrH/3,scrW/2-scrW/8,scrH/2-scrH/5))

        tk.Label(self.root,text='Username').place(x=70,y=30)
        tk.Label(self.root,text='Password').place(x=70,y=60)
        tk.Label(self.root,text='Confirm Password').place(x=70,y=90)

        self.name_input = tk.Entry(self.root, width=20, borderwidth=1)
        self.passw_input = tk.Entry(self.root, width=20, borderwidth=1, highlightthickness=1, show='*')
        self.cf_passw_input = tk.Entry(self.root, width=20, borderwidth=1, highlightthickness=1, show='*')
        self.name_input.place(x=180,y=30)
        self.passw_input.place(x=180,y=60)
        self.cf_passw_input.place(x=180,y=90)

        self.register_btn = tk.Button(self.root,text='REGISTER',width=17, justify='center', border=1, command=self.register)
        self.register_btn.place(x=180,y=150)
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

    def register(self, event = None):
        username = self.name_input.get()
        password = self.passw_input.get()
        confirm_password = self.cf_passw_input.get()

        if username != "" and password != "" and confirm_password != "":
            if password.lower() == confirm_password.lower():
                try:
                    self.user_socket.sendall(bytes(REGISTER_CODE,'utf8'))
                                       
                    self.user_socket.sendall(bytes(username,'utf8'))
                    
                    #check username already exist
                    respond = self.user_socket.recv(1)
                    flag = respond.decode('utf8')

                    # flag = 0 mean usernname is not exist
                    if flag == '0':
                        self.user_socket.send(bytes(password,'utf8'))
                        tk.messagebox.showinfo("INFO","Success!\nYour account has been created")
                    # flag = 1 mean username was exist
                    elif flag == '1':
                        tk.messagebox.showerror("ERROR","Account already exists")
                except:
                    tk.messagebox.showwarning("Warning","Oops!\nSomething went wrong.")
            else:
                tk.messagebox.showerror("ERROR","Password are not matching")

    def on_closing(self):
        self.flag_exit = True
        self.root.quit()

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()



class Login_Form():
    def __init__(self, user_socket):
        self.flag_exit = False
        self.role = -1
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.resizable(0,0)
        self.user_socket = user_socket

        scrW = self.root.winfo_screenwidth()
        scrH = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d'%(scrW/4,scrH/3,scrW/2-scrW/8,scrH/2-scrH/5))

        tk.Label(self.root,text='Username').place(x=80,y=30)
        tk.Label(self.root,text='Password').place(x=80,y=60)

        self.name_input = tk.Entry(self.root, width=20, borderwidth=1)
        self.passw_input = tk.Entry(self.root, width=20, borderwidth=1, show='*')
        self.name_input.place(x=180,y=30)
        self.passw_input.place(x=180,y=60)

        self.login_btn = tk.Button(self.root,text='LOGIN',width=17, justify='center', border=1, command=self.login)
        self.register_btn = tk.Button(self.root,text='REGISTER',width = 17,justify='center', border=1, command=self.register)
        self.login_btn.place(x=180,y=120)
        self.register_btn.place(x=180,y=150)

    def login(self, event = None):
        username = self.name_input.get()
        password = self.passw_input.get()
        flag = ""
        if username != "" and password != "":
            try:          
                self.user_socket.sendall(bytes(LOGIN_CODE,'utf8'))
                
                self.user_socket.sendall(bytes(username,'utf8'))
                r = self.user_socket.recv(100)
                self.user_socket.sendall(bytes(password,'utf8'))
                respond = self.user_socket.recv(1)
                status = respond.decode('utf8')
                #status = 0 mean user is not working now
                if status == '0':
                    respond = self.user_socket.recv(1)
                    flag = respond.decode('utf8')
                else:
                    flag = ""
            except:
                tk.messagebox.showwarning("Warning","Oops!\nSomething went wrong.")

            #No account
            if flag == '-1':
                tk.messagebox.showinfo("Show info","Account does not exist")
                self.role = -1
            #Client
            elif flag == '0':
                self.role = 0
                self.flag_exit = True
                self.root.destroy()
            #Admin
            elif flag == '1':
                self.role = 1
                self.flag_exit = True
                self.root.destroy()
            elif flag == "":
                tk.messagebox.showwarning("Warning","Your account login from another device!")

    def register(self):
        self.root.withdraw()
        r_form = Register_Form(self.user_socket)
        r_form.run()
    
        if r_form.flag_exit:
            r_form.close()
            self.root.deiconify()

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()