from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from socket import *
import sqlite3
from datetime import datetime
import crawl as C


#=============================== Define control code ===============================#
QUIT             =  'Q'
LOGIN  			 =  'L'
REGISTER         =  'R'

# admin
LIST_ALL         = 'A'
REFRESH          = 'E'

ADD_NEW          = 'N'
UPDATE           = 'U'
RELOAD           = 'D'
UPDATE_EVENT     = 'T'

#Client
SEARCH           = 'S'



#=============================== +++++++++++++++++++++++++ ===============================#

class Server(Tk):
	def __init__(self):
		super().__init__()
		# GUI
		self.on = False
		self.title("SERVER")
 
		self.fr2 = Frame(self)
		self.fr2.pack(side = RIGHT,padx = 15)

		self.fr3 = LabelFrame(self)
		self.fr3.configure(text = '--/--')
		self.fr3.pack(side = BOTTOM,padx = 10 ,pady = 5)

		self.l = Label(self.fr2,text = 'N Client',font = ('time new roman',15))
		self.l.pack(side = TOP)

		self.n_client_input = Entry(self.fr2,width = 5,font = ('time new roman',15))
		self.n_client_input.insert(0,'5')
		self.n_client_input.pack(side = TOP,padx = 5,pady = 10)

		self.status = StringVar()
		self.status.set('OFF')

		self.power_btn = Button(self.fr2,text = 'Power',font = ('time new roman',15),width = 12,height = 3, bd = 3,command = self.power)
		self.power_btn.pack(side = TOP)

		self.status_text = Label(self.fr2,text = 'STATUS:',font = ('time new roman',13))
		self.status_text.pack(side = LEFT,padx = 15)

		self.status_label = Label(self.fr2,textvariable = self.status,fg = 'red',font = ('time new roman',13))
		self.status_label.pack(side = LEFT)


		self.acces_log_detail = ttk.Treeview(self.fr3,selectmode = 'browse',height = 20)
		self.acces_log_detail.pack(side = LEFT)

		self.scoll = ttk.Scrollbar(self.fr3,orient='vertical',command = self.acces_log_detail.yview)
		self.scoll.pack(side = 'left',fill='y')

		self.acces_log_detail.configure(yscrollcommand = self.scoll.set)

		self.acces_log_detail['columns'] = ("1","2","3","4","5")
		self.acces_log_detail['show'] = 'headings'
		self.acces_log_detail.column("1",width = 100,anchor = 'c')
		self.acces_log_detail.column("2",width = 50,anchor = 'c')
		self.acces_log_detail.column("3",width = 80,anchor = 'c')
		self.acces_log_detail.column("4",width = 120,anchor = 'c')
		self.acces_log_detail.column("5",width = 50,anchor = 'c')

		self.acces_log_detail.heading("1",text = "Action")
		self.acces_log_detail.heading("2",text = "By")
		self.acces_log_detail.heading("3",text = "IP")
		self.acces_log_detail.heading("4",text = "Date and Time")
		self.acces_log_detail.heading("5",text = "Role")
		
		pass

	def power(self):
		n = 5
		x = 0
		if self.n_client_input.get() != '':
			try:
				x = int(self.n_client_input.get())
				n = x 
			except:
				x = 5
		if not self.on:  
			self.status.set('ON')
			self.status_label.configure(fg = 'green')
			self.on = True

			# khoi tao server
			self.HOST = '127.0.0.1'
			self.PORT = 12226
			self.Address = (self.HOST, self.PORT)
			self.Server = socket(AF_INET,SOCK_STREAM)
			self.Server.bind(self.Address)

			# fix lai database
			conn = sqlite3.connect('DATABASE.db')
			c = conn.cursor()
			c.execute("""
				update ACCOUNTS set STATUS_ = ? """, [0]
			)
			conn.commit()
			conn.close()

			# Write code thread here
			self.Server.listen(n)
			Z = Thread(target=self.Action)
			Z.daemon = True
			Z.start()

			#=====================


		else:
			if messagebox.askyesno('Server','Are you sure that you want to close server?'):
				self.status.set('OFF')
				self.status_label.configure(fg = 'red')
				for item in self.acces_log_detail.get_children():
					self.acces_log_detail.delete(item)
				self.on = False

				# Write code here
				# self.Server.close()

				#===============
		pass

	def run(self):
		self.mainloop()
		pass

	def Action(self):
		if self.on:
			while True:
				try:
					client , add = self.Server.accept()
					self.acces_log_detail.insert('', 'end',value = ('Connected', '' ,  add[0], self.getDateTime(),''))

					#xu li thread
					Active_client = Thread(target=self.Handle_Client, args=(client, add))
					Active_client.daemon = True
					Active_client.start()
				except Exception as e:
					print(e)
					pass
		pass

	def Handle_Client(self, client, add):
		name_ = ''
		func_ = ''
		if self.on:
			try:
				while True:
					Code = client.recv(1).decode("utf8")

					#===============START==================

					# Code: xong , Test: roi
					# Login
					if (Code == LOGIN):
						print("login")
						name_, fun_ = self.Function_Login(client)
						self.acces_log_detail.insert('', -1,value = ('Login', name_, add[0], self.getDateTime(), fun_))

					# Code: xong , Test: roi
					#Register
					elif (Code == REGISTER):
						print("Register")
						name_, fun_ = self.Funtion_Register(client)
						self.acces_log_detail.insert('',-1,value = ('Register', name_, add[0] ,self.getDateTime(), fun_))

					#================CLIENT==================
					# Code: xong , Test: oke
					elif (Code == LIST_ALL):
						try:
							# gui tat ca du lieu cho server
							print("List_all")
							conn = sqlite3.connect("DATABASE.db")
							c = conn.cursor()
							c.execute(
								"select * from MATCH"
							)
							for i in c:
								# send ID
								client.sendall(bytes(str(i[0]),'utf8'))
								client.recv(1)
								#send Min
								client.sendall(bytes(str(i[5]),'utf8'))
								client.recv(1)
								#send Club1
								client.sendall(bytes(str(i[1]),'utf8'))
								client.recv(1)
								#send Score
								client.sendall(bytes(str(i[3]),'utf8'))
								client.recv(1)
								#send Club2
								client.sendall(bytes(str(i[2]),'utf8'))
								client.recv(1)
								#send Date
								client.sendall(bytes(str(i[4]),'utf8'))
								client.recv(1)

							# send lenh de dung
							client.sendall(bytes("_END_",'utf8'))
							client.recv(1)

							conn.close() 
							self.acces_log_detail.insert('',-1,value = ('List all', name_, add[0] ,self.getDateTime(), fun_))
						except Exception as e:
							print(e)

					# Code: xong , Test: oke
					elif (Code == SEARCH):
						try:
							print("search")
							id_ = client.recv(100).decode('utf8')
							client.sendall(bytes("1", "utf8"))
							print(id_)
							# tien hanh kiem tra ID co ton tai khong
							conn = sqlite3.connect("DATABASE.db")
							c = conn.cursor()
							c.execute("select * from EVENT_MATCH where ID_MATCH = ?", [id_])
							result = c.fetchall()
							print(len(result))
							if (len(result) == 0):
								client.sendall(bytes("0", "utf8"))
								client.recv(1)
							else:
								# tien hanh thuc hien
								client.sendall(bytes("1", "utf8"))
								client.recv(1)
								# truy xuat gia tri tu Db
								c.execute("select * from MATCH where ID_MATCH = ?", [id_])
								for i in c:
									#send Min
									client.sendall(bytes(str(i[5]),'utf8'))
									client.recv(1)
									#send Club1
									client.sendall(bytes(str(i[1]),'utf8'))
									client.recv(1)
									#send Club2
									client.sendall(bytes(str(i[2]),'utf8'))
									client.recv(1)
									
								# tien hanh gui Event
								c.execute("select * from EVENT_MATCH where ID_MATCH = ? order by TIME_ asc", [id_])
								for i in c:
									#send Min
									client.sendall(bytes(str(i[2]),'utf8'))
									client.recv(1)
									#send Min
									client.sendall(bytes(str(i[1]),'utf8'))
									client.recv(1)
									#send Min
									client.sendall(bytes(str(i[3]),'utf8'))
									client.recv(1)
								#send Min
								client.sendall(bytes("_END_",'utf8'))
								client.recv(1)
							self.acces_log_detail.insert('', -1,value = ('Search', name_, add[0] ,self.getDateTime(), fun_))
						except Exception as e:
							print(e)

					# Code: xong , Test: oke
					elif (Code == REFRESH):
						try:
							print("refresh")
							# rev Date
							Date_ = client.recv(20).decode('utf8')
							client.sendall(bytes("1", 'utf8'))

							# send data to client
							conn = sqlite3.connect('DATABASE.db')
							c = conn.cursor()
							c.execute("select * from MATCH where DATE_ = ?", [Date_])

							for i in c:
								# send ID
								client.sendall(bytes(str(i[0]),'utf8'))
								client.recv(1)
								#send Min
								client.sendall(bytes(str(i[5]),'utf8'))
								client.recv(1)
								#send Club1
								client.sendall(bytes(str(i[1]),'utf8'))
								client.recv(1)
								#send Score
								client.sendall(bytes(str(i[3]),'utf8'))
								client.recv(1)
								#send Club2
								client.sendall(bytes(str(i[2]),'utf8'))
								client.recv(1)
								#send Date
								client.sendall(bytes(str(i[4]),'utf8'))
								client.recv(1)
							#Send the END
							client.sendall(bytes("_END_", "utf8"))
							client.recv(1)

							self.acces_log_detail.insert('', -1,value = ('Refresh', name_, add[0] ,self.getDateTime(), fun_))

						except Exception as e:
							print(e)

					# Code: chu , Test: oke
					#================ADMIN=================
					elif (Code == ADD_NEW):
						try:
							print("add new")
							client.sendall(bytes("1", "utf8"))
							# recv ID
							id_ = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							# recv Time
							Time_ = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							# recv Team a
							Team_a = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							# recv Score
							Score_ = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							# recv Team B
							Team_b = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							# recv Date
							Date_ = client.recv(1024).decode("utf8")
							client.sendall(bytes("1", "utf8"))

							# check ID
							conn = sqlite3.connect("DATABASE.db")
							c = conn.cursor()
							c.execute("select * from MATCH where ID_MATCH = ?", [id_])
							result = c.fetchall()
							print(len(result))
							if (len(result) != 0):
								client.sendall(bytes("1", "utf8"))
								client.recv(1)
							else:
								client.sendall(bytes("0", "utf8"))
								client.recv(1)
								
								# gan vao database
								c.execute("""
									INSERT INTO MATCH(ID_MATCH, CLUB1, CLUB2, SCORE, DATE_, TIME_SCORE) 
									VALUES (?, ?,?,?,?,?)
									""", (id_, Team_a, Team_b, Score_, Date_, Time_)
								)
							conn.commit()
							conn.close()
							self.acces_log_detail.insert('', -1,value = ('Add new', name_, add[0] ,self.getDateTime(), fun_))

						except Exception as e:
							print(e)
						
					# Code: chua , Test: chua
					elif (Code == UPDATE):
						try:
							client.sendall(bytes("1", "utf8"))
							print("update")
							id_ = client.recv(1048).decode("utf8")
							#client.sendall(bytes("1", "utf8"))
							# check ID
							conn = sqlite3.connect("DATABASE.db")
							c = conn.cursor()
							c.execute("select * from MATCH where ID_MATCH = ?", [id_])
							result = c.fetchall()
							if (len(result) != 0):
								client.sendall(bytes("1", "utf8"))
								client.recv(1)
								print("oke nhe nguoi anh em")
								
								client.sendall(bytes(str(result[0][1]), "utf8"))
								client.recv(1)

								client.sendall(bytes(str(result[0][2]), "utf8"))
								client.recv(1)
							else:
								client.sendall(bytes("0", "utf8"))
								client.recv(1)
							conn.commit()
							conn.close()
							self.acces_log_detail.insert('', -1,value = ('Update', name_, add[0] ,self.getDateTime(), fun_))

						except Exception as e:
							print(e)

					elif (Code == UPDATE_EVENT):
						try:
							print("update event")

							# recv data
							id_ = client.recv(1048).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							club_ = client.recv(1048).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							time_ = client.recv(1048).decode("utf8")
							client.sendall(bytes("1", "utf8"))
							event_ = client.recv(1048).decode("utf8")
							client.sendall(bytes("1", "utf8"))

							# insert vao date base
							try:
								conn = sqlite3.connect("DATABASE.db")
								c = conn.cursor()
								c.execute("""insert into EVENT_MATCH(ID_MATCH, CLUB, TIME_, EVENT_)
											values (?, ?, ?, ?)
								""", (id_, club_, time_, event_)
								)
								client.sendall(bytes("1", "utf8"))
								client.recv(1)

								conn.commit()
								conn.close()

							except Exception as e:
								print(e)
								client.sendall(bytes("0", "utf8"))
								client.recv(1)
							self.acces_log_detail.insert('', -1,value = ('Update_Event', name_, add[0] ,self.getDateTime(), fun_))

						except Exception as e:
								print(e)

					# Code: xong , Test: oke
					elif (Code == RELOAD):
						try:
							try:
								S = C.Crawl()
								S.Run()
								S.Commit()

								client.sendall(bytes("0", "utf8"))
								client.recv(1)
							except:
								client.sendall(bytes("1", "utf8"))
								client.recv(1)

							self.acces_log_detail.insert('', -1,value = ('Reload', name_, add[0] ,self.getDateTime(), fun_))
						except Exception as e:
							print(e) 

					elif (Code == QUIT):
						try:
							conn = sqlite3.connect("DATABASE.db")
							c = conn.cursor()
							c.execute("""
								update ACCOUNTS set STATUS_ = ? where USERNAME_ = ?
							""", (0, name_)
							)
							conn.commit()
							conn.close()
						except Exception as e:
							print(e)
						self.acces_log_detail.insert('', -1,value = ('Quit', name_, add[0] ,self.getDateTime(), fun_))

			except Exception as e:
				print(e)
				try:
					conn = sqlite3.connect("DATABASE.db")
					c = conn.cursor()
					c.execute("""
						update ACCOUNTS set STATUS_ = ? where USERNAME_ = ?
					""", (0, name_)
					)
					conn.commit()
					conn.close()
				except Exception as e:
					print(e)
				self.acces_log_detail.insert('', 'end',value = ('Quit', name_, add[0] ,self.getDateTime(), fun_))

				print("Close")
				client.close()

		pass

	def Function_Login(self, client):
		name1 = client.recv(100)
		name = name1.decode("utf8")
		client.sendall(bytes("r","utf8"))

		password1 = client.recv(100)
		password = password1.decode("utf8")

		# check login
		value = self.Check_Login(name, password)
		# gui value cho Client
		client.sendall(bytes(str(value), "utf8"))

		# return name va function
		if (value == 0):
			return name, "Client"
		elif (value == 1):
			return name, "Admin"
		else:
			return '', ''

	def Check_Login(self, name, password):
		# check trang thai
		value = 0

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
			if (role == "Client"):
				value =  0
			else: 
				value = 1
			if (status):
				value =  2
		else:
			value = 3
		# thay doi trang thai status trong database
		if (value == 1 or value == 0):
			cursor.execute(
				"UPDATE ACCOUNTS  SET STATUS_ = '1' where USERNAME_ = ? and PASSWORD_ = ? ", (name, password)
			)

		conn.commit()
		conn.close()
		
		return value
	
	def Funtion_Register(self, client):
		conn = sqlite3.connect('DATABASE.db')

		user_name = client.recv(20).decode("utf8")

		# check a name exitting in sql
		cursor = conn.cursor()
		cursor.execute(
			"select count(*) from ACCOUNTS as un where un.USERNAME_ = ?" , [user_name]
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
			 	"select count(*) from ACCOUNTS un where un.USERNAME_ = ?", [user_name]
		    )
			# nhan password
			password = client.recv(20).decode("utf8")
			# gui gia tri vao sql
			cursor.execute(
				"insert into ACCOUNTS(USERNAME_, PASSWORD_, ROLE_, STATUS_) values(?, ?, ?, ?)",
				(user_name, password, "Client", 0)
			)
			conn.commit()
		else:
			client.sendall(bytes("1", "utf8"))

		conn.close()
		if (check):
			return user_name, "Client"
		else:
			return '', ''

	def getDateTime(self):
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		return dt_string

if __name__ == "__main__":
	s = Server()
	s.run()