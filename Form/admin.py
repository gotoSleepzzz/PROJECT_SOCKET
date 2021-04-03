from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk

class Admin_Form():
    def __init__(self,user_socket):
        self.flag_logout = False
        self.flag_exit = False
        self.user_socket = user_socket
        self.root = tk.Toplevel()
        self.root.geometry("1300x700+150+50")

        self.logout_btn = tk.Button(self.root,text='LOGOUT',width=17, justify='center', border=1, command=self.logout)
        self.logout_btn.place(x=180,y=120)


        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        pass

    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.flag_logout = False
            self.flag_exit = True
            self.root.quit()
        pass

    def close(self):
        self.root.destroy()

    def logout(self):
        self.flag_exit = True
        self.flag_logout = True
        self.root.quit()
        pass

    def run(self):
        self.flag_logout = False
        self.flag_exit = False
        self.root.mainloop()
