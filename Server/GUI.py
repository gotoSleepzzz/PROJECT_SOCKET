from tkinter import *
from PIL import ImageTk, Image
import pyodbc
import socket
from threading import Thread
import threading
import time

stop_thread = False

class GUI2:
	def __init__( self):
		self.w = Tk()

		scW = self.w.winfo_screenwidth()
		scH = self.w.winfo_screenheight()

		self.w.geometry("800x500+%d+%d" %(scW/2 - 450, scH/2 - 350))
		self.w.resizable(width=False, height=False)

		self.messages_frame = Frame(self.w, bg='green')
		self.messages_frame.pack(side=LEFT)
		self.scrollbar = Scrollbar(self.messages_frame)
		self.msg_list = Listbox(self.messages_frame, height=200, width=70, yscrollcommand=self.scrollbar.set)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.msg_list.pack(side=LEFT, fill=BOTH)
		self.msg_list.pack()
		self.msg_list.config(yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.msg_list.yview)

		# tao Server
		self.Host = "127.0.0.1"
		self.Port = 6111
		self.Address = (self.Host, self.Port)
		self.Size = 100
		self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Server.bind(self.Address)

		# tao tuple luu client va address
		self.Clients = {}
		self.Address_client = {}
		# tao ket noi voi SQL_SERVER(LIVE_SCORE)
		self.conn = pyodbc.connect(
			"driver={SQL Server Native Client 11.0};"
			"Server=MAYTINH-CD1NVG5\SQLEXPRESS;"
			"Database=LIVE_SCORE;"
			"Trusted_Connection=yes"
			)

	def Insert_msg(self, msg):
		self.msg_list.insert(END, msg)

	def Run_mainloop(self):
		threading.Thread(target=self.Run_Server).start()
		self.w.protocol("WM_DELETE_WINDOW", self.close)
		self.w.mainloop()
	# test : oke
	def Action(self):
		try:
			while (True):
				client, add = self.Server.accept()
				mess = str(add) + " connected to Server"
				self.Insert_msg(mess)

				Active_client = threading.Thread(target=self.Handle_Client, args=(client,))
				Active_client.start()
				global stop_thread
				if stop_thread:
					print(1)
					break
				Active_client.join()
		except:
			tempt = 1	
	#test : 
	def Handle_Client(self, client):
			# Nhan lenh tu client
			while(True):
				global stop_thread
				if (stop_thread):
					print(12)
					break
				Code = client.recv(1).decode("utf8")
				if (Code == '1'):

					#print(Code)
					self.Insert_msg("1")

					self.Function_Login(client)
				elif (Code == '2'):
					#print(Code)

					self.Insert_msg("2")
					self.Funtion_Register(client)  

	def Function_Login(self, client):
		# nhan name va password cua client
		name1 = client.recv(self.Size)
		name = name1.decode("utf8")
		client.sendall(bytes("r","utf8"))
		self.Insert_msg(name)
		#print(name)

		password1 = client.recv(self.Size)
		password = password1.decode("utf8")
		#print(password)
		self.Insert_msg(password)


		# check login
		value = self.Check_Login(name, password)

		#print("Value:" + str(value))
		tempt = "Value:" + str(value)
		self.Insert_msg(tempt)

		if (value == -1):
			client.sendall(bytes(str(value), "utf8"))
		else:
			client.sendall(bytes(str(value), "utf8"))

	# ham tra ve 0: client , 1:admin , -1: khong ton tai password		
	def Check_Login(self, name, password):
		cursor = self.conn.cursor()
		cursor.execute(
			"select count(*) from ACCOUNT as un where un.USERNAME_ = ? and un.PASSWORD_= ?",(name,password)
			)
		# check account co xuat hien trong database hay khong
		for i in cursor:
			if (i[0] == 1):
				check = True
			else:
				check = False
		if (check == True):
			cursor.execute(
				"select un.ROLE_, un.STATUS_ from ACCOUNT as un where un.USERNAME_ = ? and un.PASSWORD_= ?",(name,password)
				)
			for i in cursor:
				status = i[1]
				role = i[0]
			if (status):
				self.Insert_msg("status")
				return 2
			if (role == "Client"):
				return 0
			else: 
				return 1
		else:
			return 3

	def Funtion_Register(self, client):
		global conn
		user_name = client.recv(20).decode("utf8")
		#print(user_name)
		self.Insert_msg(user_name)
	    # check a name exitting in sql
		cursor = self.conn.cursor()
		cursor.execute(
			"select count(*) from ACCOUNT as un where un.USERNAME_ = ?" , user_name
			)
		check = True
		for i in cursor:
			if (i[0] != 0):
				check = False
				break
		if (check):
			# gui gia tri tra ve cho client
			client.sendall(bytes("0", "utf8"))
			cursor.execute(
				"select count(*) from ACCOUNT un where un.USERNAME_ = ?", user_name
				)
			# nhan password
			password = client.recv(20).decode("utf8")
			# gui gia tri vao sql
			cursor.execute(
				"insert into ACCOUNT(USERNAME_, PASSWORD_, ROLE_, STATUS_) values(?, ?, ?, ?)",
				user_name, password, "Client", False
				)
			cursor.commit()
		else:
			client.sendall(bytes("1", "utf8"))  
    
	def Run_Server(self):
		self.Server.listen(5)
		self.Insert_msg("Wait Client!!!")
		try:
			Start = threading.Thread(target=self.Action)
			Start.start()
			Start.join()
		except:
			print("loi")

	def close(self):
		global stop_thread
		stop_thread = True


		self.Server.close()
		self.conn.close()
		self.w.destroy()

class GUI_SERVER:
	def __init__(self):
		self.win = Tk()
		self.win.title('SERVER')
		scW = self.win.winfo_screenwidth()
		scH = self.win.winfo_screenheight()

		self.win.geometry("800x500+%d+%d" %(scW/2 - 450, scH/2 - 350))
		self.win.resizable(width=False, height=False)

	def Run(self):
		#picture
		my_canvas = Canvas(self.win, width=800, height=500)
		my_canvas.pack()
		img = ImageTk.PhotoImage(Image.open("Image/bong.png"))
		my_image = my_canvas.create_image(0, 0, anchor=NW, image=img)
		#button
		img_Button = ImageTk.PhotoImage(Image.open("Image/start.png"), width= 100, height=100 )
		my_button = Button(self.win, width=300, height=100,image=img_Button,  command=self.CauNoi)
		my_button.place(x=250, y=50)

		self.win.protocol("WM_DELETE_WINDOW", self.close)
		self.win.mainloop()
	def CauNoi(self):
		self.win.destroy()
		S2 = GUI2()
		S2.Run_mainloop()

	def close(self):
		self.win.destroy()

