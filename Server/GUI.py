from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
import Server as SO

class GUI2:
	def __init__(   self):

		self.w = Tk()

		scW = self.w.winfo_screenwidth()
		scH = self.w.winfo_screenheight()

		self.w.geometry("800x500+%d+%d" %(scW/2 - 450, scH/2 - 350))
		self.w.resizable(width=False, height=False)

		self.messages_frame = Frame(self.w)
		self.messages_frame.pack(side=LEFT)
		self.scrollbar = Scrollbar(self.messages_frame)
		self.msg_list = Listbox(self.messages_frame, height=200, width=70, yscrollcommand=self.scrollbar.set)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.msg_list.pack(side=LEFT, fill=BOTH)
		self.msg_list.pack()
		self.msg_list.config(yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.msg_list.yview)
		
	def Insert_msg(self, msg):
		self.msg_list.insert(END, msg)
	def Run_mainloop(self):
		self.w.mainloop()

class GUI_SERVER:
	def __init__(self):
		self.win = Tk()
		scW = self.win.winfo_screenwidth()
		scH = self.win.winfo_screenheight()

		self.win.geometry("800x500+%d+%d" %(scW/2 - 450, scH/2 - 350))
		self.win.resizable(width=False, height=False)

	def Run(self):
		#picture
		my_canvas = Canvas(self.win, width=800, height=500)
		my_canvas.pack()
		img = ImageTk.PhotoImage(Image.open("bongda.png"))
		my_image = my_canvas.create_image(0, 0, anchor=NW, image=img)
		#button
		my_button = Button(self.win, text="START SERVER", width=25, height=3, command=self.CauNoi)
		my_button.place(x=70, y=110)
		self.win.mainloop()
	def CauNoi(self):
		global Messenge
		global Check_code

		self.win.destroy()
		S2 = GUI2()
		
		#chay server
		ser = SO.SERVER(S2)
		Thread(target=ser.Run_Server).start()

		S2.Run_mainloop()

S1 = GUI_SERVER()
S1.Run()

