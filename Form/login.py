import tkinter as tk
from tkinter import messagebox
import socket

LOGIN_CODE = '1'
REGISTER_CODE = '2'

class Register_Form():
    def __init__(self,server_address):
        self.flag_exit = False  #to check window close
        self.root = tk.Toplevel()
        self.server_address = server_address
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

        self.register_btn = tk.Button(self.root,text='REGISTER',width=18, justify='center', border=1, command=self.register)
        self.register_btn.place(x=180,y=150)
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.root.mainloop()

    def register(self, event = None):
        username = self.name_input.get()
        password = self.passw_input.get()
        confirm_password = self.cf_passw_input.get()

        if username != "" and password != "" and confirm_password != "":
            if password.lower() == confirm_password.lower():
                try:
                    s = socket.socket(sock.AF_INET,socket.SOCK_STREAM)
                    s.connect(self.server_address)

                    s.send(bytes(username,'utf8'))
                    
                    #check username already exist
                    respond = s.recv(1)
                    flag = respond.decode('utf8')

                    # flag = 0 mean usernname is not exist
                    if flag == '0':
                        s.send(bytes(password,'utf8'))
                        tk.messagebox.showinfo("INFO","Success!\nYour account has been created")
                    # flag = 1 mean username was exist
                    elif flag == '1':
                        tk.messagebox.showerror("ERROR","Account already exists")
                except:
                    tk.messagebox.showwarning("Warning","Oops!\nSomething went wrong.")
                finally:
                    s.close()
            else:
                tk.messagebox.showerror("ERROR","Password are not matching")



    def on_closing(self):
        self.flag_exit = True
        self.root.quit()

    def close(self):
        self.root.destroy()



class Login_Form():
    def __init__(self, Host, Port):
        self.flag_exit = False
        self.role = -1
        self.root = tk.Tk()
        self.root.title("LOGIN")
        self.root.resizable(0,0)
        self.server_address = (Host,Port)

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
        self.root.mainloop()

    def login(self, event = None):
        username = self.name_input.get()
        password = self.passw_input.get()
        if username != "" and password != "":
            try:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(self.server_address)
                
                s.sendall(bytes(LOGIN_CODE,'utf8'))
                
                s.sendall(bytes(username,'utf8'))
                r = s.recv(100)
                s.sendall(bytes(password,'utf8'))
                respond = s.recv(100)
                flag = respond.decode('utf8')
                
                print(flag)
            except:
                tk.messagebox.showwarning("Warning","Oops!\nSomething went wrong.")
            finally:
                s.close()

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
            else:
                self.role = 1
                self.flag_exit = True
                self.root.destroy()

    def register(self):
        self.root.withdraw()
        r_form = Register_Form(self.server_address)
    
        if r_form.flag_exit:
            print("exit")
            r_form.close()
            self.root.deiconify()

    def close(self):
        self.root.destroy()
