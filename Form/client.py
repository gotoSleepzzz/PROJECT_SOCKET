from tkinter import *
from tkinter import messagebox
import tkinter as tk

class Client_Form():
    def __init__(self):
        self.flag_exit = False
        self.flag_logout = False
        self.root = tk.Tk()
        self.root.geometry("1300x700+150+50")
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        pass

    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
        pass

    def run(self):
        self.flag_exit = False
        self.flag_logout = False
        self.root.mainloop()