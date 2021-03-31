import pyodbc
import socket
from threading import Thread
import threading

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


def Function_Login(client):
	# nhan name va password cua client
	name1 = client.recv(Size)
	name = name1.decode("utf8")
	client.sendall(bytes("r","utf8"))
	print(name)

	password1 = client.recv(Size)
	password = password1.decode("utf8")
	print(password)

	# check login
	value = Check_Login(name, password)
	if (value == -1):
		#gui du lieu di client
		client.sendall(bytes(str(value), "utf8"))
	else:
		client.sendall(bytes(str(value), "utf8"))

# ham tra ve 0: client , 1:admin , -1: khong ton tai password
def Check_Login(name, password):
	cursor = conn.cursor()
	cursor.execute(
		"select count(*) from USER_NAME as un where un.NAME = ? and un.PASS= ?",(name,password)
	)
	for i in cursor:
		if (i[0] == 1):
			check = True
		else:
			check = False
	if (check == True):
		cursor.execute(
			"select un.ROLE_ from USER_NAME as un where un.NAME = ? and un.PASS= ?",(name,password)
		)
		for i in cursor:
			Value = i[0]
		return Value
	else:
		return -1

# tao ket noi voi SQL_SERVER(LIVE_SCORE)
conn = pyodbc.connect(
	"driver={SQL Server Native Client 11.0};"
	"Server=MAYTINH-CD1NVG5\SQLEXPRESS;"
	"Database=LIVE_SCORE;"
	"Trusted_Connection=yes"
)
# tao socket server
Host = ''
Port = 61113
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



