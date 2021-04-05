import login as lg
import admin as ad
import client as cl
import tkinter as tk
import socket

HOST = "127.0.0.1"
PORT = 61111
server_address = (HOST,PORT)
global user
try:
    user_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_socket.connect(server_address)

    login = lg.Login_Form(user_socket)

    while True:
        login.run()

        if login.flag_exit:
            if login.role == -1:
                print("LOGIN FAILED")
            elif login.role == 0:
                print("YOU'RE CLIENT")
                user = cl.Client_Form(user_socket)
            elif login.role == 1:
                print("YOU'RE ADMIN")
                user = ad.Admin_Form(user_socket)

        user.run()

        if user.flag_exit:
            if not user.flag_logout:
                break

    user_socket.close()
except:
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showwarning("Warning","Check your connection!")
