import login as lg
import admin as ad
import client as cl
import tkinter as tk
import socket

HOST = "127.0.0.1"
PORT = 61234
server_address = (HOST,PORT)
root = tk.Tk()
root.withdraw()
global user

try:
    user_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_socket.connect(server_address)
    user = lg.Login_Form(user_socket)
    while True:
        user.run()
        if user.role == 1:
            print("YOU ARE ADMIN")
            user.close()
            user = ad.Admin_Form(user_socket)
        elif user.role == 0:
            print("YOU ARE CLIENT")
            user.close()
            user = cl.Client_Form(user_socket)
        elif user.role == -1:
            user.close()
            break
        user.run()
        if user.flag_exit:
            if user.flag_logout == False:
                user.close()
                break
            else:
                user.close()
                user = lg.Login_Form(user_socket)

    user_socket.close()
except Exception as e:
    print(e)
    tk.messagebox.showwarning("Warning","Oops\nSomething went wrong!")
