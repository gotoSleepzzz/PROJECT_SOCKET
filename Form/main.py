import login as lgform
import tkinter as tk

login = lgform.Login_Form()

login.run()

if login.Role() == 1 or login.Role() == 0:
    print("LOGIN SUCCESSFULL")
