import pyodbc
import socket
from threading import Thread
import threading
import time

class SERVER():
	def __init__(self, S2):
		# tao socket server
		self.S2 = S2
		self.Host = "127.0.0.1"
		self.Port = 61111
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
	# test : oke
	def Action(self):
		while (True):
			client , add = self.Server.accept()
			
			#print
			mess = str(add) + " connected to Server"
			self.S2.Insert_msg(mess)

			#xu li thread
			Active_client = threading.Thread(target=self.Handle_Client, args=(client,))
			Active_client.start()
	
	#test : 
	def Handle_Client(self, client):
			# Nhan lenh tu client
			while(True):
				Code = client.recv(1).decode("utf8")
				if (Code == '1'):

					#print(Code)
					self.S2.Insert_msg("1")

					self.Function_Login(client)
				elif (Code == '2'):
					#print(Code)

					self.S2.Insert_msg("2")
					self.Funtion_Register(client)  
	# test: oke
	def Function_Login(self, client):
		# nhan name va password cua client
		name1 = client.recv(self.Size)
		name = name1.decode("utf8")
		client.sendall(bytes("r","utf8"))
		self.S2.Insert_msg(name)
		#print(name)

		password1 = client.recv(self.Size)
		password = password1.decode("utf8")
		#print(password)
		self.S2.Insert_msg(password)


		# check login
		value = self.Check_Login(name, password)

		#print("Value:" + str(value))
		tempt = "Value:" + str(value)
		self.S2.Insert_msg(tempt)

		if (value == -1):
			client.sendall(bytes(str(value), "utf8"))
		else:
			client.sendall(bytes(str(value), "utf8"))

	# ham tra ve 0: client , 1:admin , -1: khong ton tai password
	# test : oke		
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
				self.S2.Insert_msg("status")
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
		self.S2.Insert_msg(user_name)
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
    
    #oke 
	def Run_Server(self):
		self.Server.listen(5)
		self.S2.Insert_msg("Wait Client!!!")

		Start = threading.Thread(target=self.Action)
		Start.start()
		Start.join()

	def __del__(self):
		self.Server.close()
		self.conn.close()
