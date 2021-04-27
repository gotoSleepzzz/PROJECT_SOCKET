import socket
from threading import Thread
import threading
import sqlite3

def Action():
	while (True):
		client , add = Server.accept()
		print('%s:%s connected to Server' %add)
		#xu li thread
		Active_client = threading.Thread(target=Handle_Client, args=(client,))
		Active_client.start()

def Handle_Client(client):
	# Nhan lenh tu client
	while(True):
		Code = client.recv(1).decode("utf8")
		if (Code == '1'):
			print(Code)
			Function_Login(client)
		elif (Code == '2'):
			print(Code)
			Funtion_Register(client)

def Function_Login(client):
	# try:		
	# 	# nhan name va password cua client
	# 	name1 = client.recv(Size)
	# 	name = name1.decode("utf8")
	# 	client.sendall(bytes("r","utf8"))
	# 	print(name)

	# 	password1 = client.recv(Size)
	# 	password = password1.decode("utf8")
	# 	print(password)

	# 	# check login
	# 	value = Check_Login(name, password)
	# 	print("Value:" + str(value))
	# 	if (value == -1):
	# 		#gui du lieu di client
	# 		client.sendall(bytes(str(value), "utf8"))
	# 	else:
	# 		client.sendall(bytes(str(value), "utf8"))
	# except:
	# 	print("loi trong Function_Login")
		# 	# nhan name va password cua client
	name1 = client.recv(Size)
	name = name1.decode("utf8")
	client.sendall(bytes("r","utf8"))
	print(name)

	password1 = client.recv(Size)
	password = password1.decode("utf8")
	print(password)

	# check login
	value = Check_Login(name, password)
	print("Value:" + str(value))
	if (value == -1):
		#gui du lieu di client
		client.sendall(bytes(str(value), "utf8"))
	else:
		client.sendall(bytes(str(value), "utf8"))

# ham tra ve 0: client , 1:admin , -1: khong ton tai password
def Check_Login(name, password):
	conn = sqlite3.connect('DATABASE.db')

	cursor = conn.cursor()
	cursor.execute(
		"select count(*) from ACCOUNTS as un where un.USERNAME_ = ? and un.PASSWORD_= ?",(name,password)
	)
	# check account co xuat hien trong database hay khong
	for i in cursor:
		if (i[0] == 1):
			check = True
		else:
			check = False

	if (check == True):
		cursor.execute(
			"select un.ROLE_, un.STATUS_ from ACCOUNTS as un where un.USERNAME_ = ? and un.PASSWORD_= ?",(name,password)
		)
		# check trang thai hoat dong cua no
		for i in cursor:
			status = i[1]
			role = i[0]
			print(i[0])
			print(i[1])
			print(i[0] == "Admin")
		if (status):
			print("status")
			return 2
		if (role == "Client"):
			return 0
		else: 
			return 1
	else:
		return 3
	conn.close()

def Funtion_Register(client):
	conn = sqlite3.connect('DATABASE.db')

	user_name = client.recv(20).decode("utf8")
	print(user_name)
	# check a name exitting in sql
	cursor = conn.cursor()
	cursor.execute(
		"select count(*) from ACCOUNTS as un where un.USERNAME_ = ?" , user_name
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
		 	"select count(*) from ACCOUNTS un where un.USERNAME_ = ?", user_name
	    )
		# nhan password
		password = client.recv(20).decode("utf8")
		# gui gia tri vao sql
		cursor.execute(
			"insert into ACCOUNTS(USERNAME_, PASSWORD_, ROLE_, STATUS_) values(?, ?, ?, ?)",
			user_name, password, "Client", False
		)
		cursor.commit()
	else:
		client.sendall(bytes("1", "utf8"))
	conn.close()


# tao socket server
Host = ""
Port = 61222
Address = (Host, Port)
Size = 100

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(Address)

# tao tuple luu client va address
Clients = {}
Address_client = {}

if __name__ == "__main__":
	Server.listen(5)
	print("Wait Client!!!")
	Start = threading.Thread(target=Action)

	Start.start()
	Start.join()

	Server.close()
	conn.close()