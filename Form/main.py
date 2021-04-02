import login as lgform
import tkinter as tk

HOST = "127.0.0.1"
PORT = 125000

login = lgform.Login_Form(HOST,PORT)

if login.flag_exit:
    if login.role == -1:
        print("LOGIN FAILED")
        
    elif login.role == 0:
        print("YOU'RE CLIENT")
    elif login.role == 1:
        print("YOU'RE ADMIN")
