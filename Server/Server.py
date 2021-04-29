from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from socket import *
import sqlite3
from datetime import datetime

# def on_closing():
# 	Server.close()
# 	window.destroy()

class Server(Tk):
	def __init__(self):
		super().__init__()
		# khoi tao server
		self.HOST = '127.0.0.1'
		self.PORT = 12226
		self.Address = (self.HOST, self.PORT)
		self.Server = socket(AF_INET,SOCK_STREAM)
		self.Server.bind(self.Address)

		# GUI
		self.on = False
		self.title("SERVER")
 
		self.fr2 = Frame(self)
		self.fr2.pack(side = RIGHT,padx = 15)

		self.fr3 = LabelFrame(self)
		self.fr3.configure(text = '--/--')
		self.fr3.pack(side = BOTTOM,padx = 10 ,pady = 5)


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
		if not self.on:  
			self.status.set('ON')
			self.status_label.configure(fg = 'green')
			self.on = True

			# Write code thread here
			self.Server.listen(5)
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
				self.Server.close()

				#===============
		pass

	def run(self):
		self.mainloop()
		pass

	def Action(self):
		while (True):
			try:
				client , add = self.Server.accept()
				self.acces_log_detail.insert('', 'end',value = ('Connected', str(add[1]) ,  add[0], self.getDateTime(),''))

				#xu li thread
				Active_client = Thread(target=self.Handle_Client, args=(client, add))
				Active_client.daemon = True
				Active_client.start()
			except Exception as e:
				print(e)
				pass
		pass

	def Handle_Client(self, client, add):
		try:
			name_ = ''
			func_ = ''
			while True:
				Code = client.recv(1).decode("utf8")
				# Login
				if (Code == '1'):
					print("login")
					name_, fun_ = self.Function_Login(client)
					self.acces_log_detail.insert('', 'end',value = ('Login', name_, add[0], self.getDateTime(), fun_))

				#Register
				elif (Code == '2'):
					print("Register")
					name_, fun_ = self.Funtion_Register(client)
					self.acces_log_detail.insert('', 'end',value = ('Register', name_, add[0], self.getDateTime(), fun_))
		except Exception as e:
			print(e)
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
			if (status):
				value =  2
			if (role == "Client"):
				value =  0
			else: 
				value = 1
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