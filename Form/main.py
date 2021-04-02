import login as lg
import tkinter as tk
import socket

HOST = "127.0.0.1"
PORT = 55666
server_address = (HOST,PORT)
try:
    user_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_socket.connect(server_address)

    login = lg.Login_Form(user_socket)
    login.run()

    if login.flag_exit:
        if login.role == -1:
            print("LOGIN FAILED")
        elif login.role == 0:
            print("YOU'RE CLIENT")
        elif login.role == 1:
            print("YOU'RE ADMIN")
    user_socket.close()
except:
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showwarning("Warning","Check your connection!")
