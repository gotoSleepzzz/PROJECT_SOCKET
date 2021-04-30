from tkinter    import *
from tkinter    import messagebox
from tkinter    import ttk
from PIL        import ImageTk, Image
from datetime   import datetime
from tkcalendar import DateEntry
from calendar   import monthrange
import socket

PORT = 12226

LOGIN                   =    'L'
REGISTER                =    'R'
SEARCH                  =    'S'
REFRESH                 =    'E'
LISTALL                 =    'A'
UPDATE                  =    'U'

class Admin(Toplevel):
    def __init__(self,user_socket,master = None):
        super().__init__(master)
        self.master = master
        self.user_socket = user_socket

        self.master.withdraw()
        self.grab_set()
        self.title('Live Score - ADMIN')
        self.iconbitmap('icon.ico')
        self.geometry("850x650+250+50")
        self.configure(background = 'SeaGreen')
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        img = PhotoImage(file = 'logout.png')
        logout_img = img.subsample(2,2)
        self.logout_btn = Button(self,text = 'LOGOUT',bd=1,width = 80,height = 30,image = logout_img,compound = LEFT,command = self.logout)
        self.logout_btn.image = logout_img
        self.logout_btn.pack(side = TOP,anchor = NE,padx = 5,pady = 5)

        self.frL = Frame(self,bg  = 'LimeGreen')
        self.frL.pack(side = LEFT,padx = 70)

        self.frR = Frame(self,bg  = 'LimeGreen')
        self.frR.pack(side = RIGHT,padx = 10)

        self.fr1 = Frame(self.frL,bg  = 'LimeGreen')
        self.fr1.pack()

        self.l = Label(self.fr1,text = 'Score ID: ',fg = 'LightBlue',bg = 'white',bd=0,font = ('time new roman',20))
        self.l.pack(side = LEFT)

        self.score_id_input = Entry(self.fr1,bd=0,width = 25,font =('time new roman',21))
        self.score_id_input.pack(side = LEFT)

        img = PhotoImage(file = 'search.png')
        search_img = img.subsample(1,1)
        self.search_btn = Button(self.fr1,bd = 1,image = search_img,compound = LEFT,command = self.search)
        self.search_btn.image = search_img
        self.search_btn.pack(side = LEFT)

        self.fr2 = Frame(self.frL,bg  = 'LimeGreen')
        self.fr2.pack(pady = 10,padx = 20)

        img = PhotoImage(file = 'previous.png')
        previous_img = img.subsample(2,2)
        self.previous_btn = Button(self.fr2,bd = 1,image = previous_img,compound = LEFT,command = self.predate)
        self.previous_btn.image = previous_img
        self.previous_btn.pack(side = LEFT)
        
        self.cal = DateEntry(self.fr2, width=12,font = 15, background='Green',foreground='white', bd=2,date_pattern='dd/mm/y')
        self.cal.pack(side = LEFT,padx=10, pady=10)

        img = PhotoImage(file = 'next.png')
        next_img = img.subsample(2,2)
        self.next_btn = Button(self.fr2,bd = 1,image = next_img,compound = LEFT,command = self.nextdate)
        self.next_btn.image = next_img
        self.next_btn.pack(side = LEFT)

        img = PhotoImage(file = 'refresh.png')
        refresh_img = img.subsample(2,2)
        self.refresh_btn = Button(self.fr2,bd = 1,image = refresh_img,compound = LEFT,command = self.refresh)
        self.refresh_btn.image = refresh_img
        self.refresh_btn.pack(side = LEFT,padx = 5)

        self.fr3 = Frame(self.frL,bg = 'LimeGreen')
        self.fr3.pack()

        self.list_all = ttk.Treeview(self.fr3,selectmode = 'browse',height = 20)
        self.list_all.pack(side= LEFT)

        self.scoll = ttk.Scrollbar(self.fr3,orient='vertical',command = self.list_all.yview)
        self.scoll.pack(side = 'left',fill='y')

        self.list_all.configure(yscrollcommand = self.scoll.set)

        self.list_all['columns'] = ("1","2","3","4","5","6")
        self.list_all['show'] = 'headings'
        self.list_all.column("1",width = 50,anchor = 'c')
        self.list_all.column("2",width = 50,anchor = 'c')
        self.list_all.column("3",width = 150,anchor = 'c')
        self.list_all.column("4",width = 50,anchor = 'c')
        self.list_all.column("5",width = 150,anchor = 'c')
        self.list_all.column("6",width = 100,anchor = 'c')

        self.list_all.heading("1",text = "ID")
        self.list_all.heading("2",text = "Time")
        self.list_all.heading("3",text = "Team 1")
        self.list_all.heading("4",text = "Ti so")
        self.list_all.heading("5",text = "Team 2")
        self.list_all.heading("6",text = "Date")

        self.list_all_btn = Button(self.frR,bd= 1,text = '  List All  ',font=('time new roman',15),command = self.listAll)
        self.list_all_btn.pack(side = TOP,padx = 15,pady = 15)
        self.add_new_btn = Button(self.frR,bd= 1,text = ' Add new  ',font=('time new roman',15),command = self.addNew)
        self.add_new_btn.pack(side = TOP,padx = 15,pady = 15)
        self.update_btn = Button(self.frR,bd= 1,text = '  Update  ',font=('time new roman',15),command =self.update)
        self.update_btn.pack(side = TOP,padx = 15,pady = 15)
        self.reload_btn = Button(self.frR,bd= 1,text = '  Reload  ',font=('time new roman',15),command =self.reload)
        self.reload_btn.pack(side = TOP,padx = 15,pady = 15)

        self.list_all.insert('', 'end',value = ('CL11','FT','Chelsea','1 - 1','Real Madrid','28/04/2021'))
        self.list_all.insert('', 'end',value = ('CL11','89\'','Liverpool','1 - 1','Barcelona','28/04/2021'))
        self.list_all.insert('', 'end',value = ('CL11','HT','Chelsea','1 - 1','Arsenal','28/04/2021'))

    def listAll(self):
        try:
            self.user_socket.sendall(bytes(LISTALL,'utf8'))
            self.user_socket.recv(1).decode('utf8')

            for i in self.list_all.get_children():
                self.list_all.delete(i)
            while True:
                id_ = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                if id_ == '_END_':
                    break
                time = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamA = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                score = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamB = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                date = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                self.list_all.insert('', 'end' ,value = (id_,time,teamA,score,teamB,date))
            
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!')
        pass

    def addNew(self):
        try:
            def add():
                self.user_socket.sendall(bytes(ADDNEW,'utf8'))
                self.user_socket.recv(1)    
                self.user_socket.sendall(bytes(id_.get(),'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(time.get(),'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(teamA.get(),'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(score.get(),'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(teamB.get(),'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(cal.get_date().year,'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(cal.get_date().month,'utf8'))
                self.user_socket.recv(1)
                self.user_socket.sendall(bytes(cal.get_date().day,'utf8'))

                flag = self.user_socket.recv(1)

                if flag == '0':
                    messagebox.showinfo('System','Add new success!')
                elif flag == '1':
                    messagebox.showwarning('System','Score Id was exists')
                pass
            t = Toplevel()
            t.grab_set()
            id_ = Entry(t,bd=0,width = 25,font =('time new roman',21))
            id_.insert(0,'Score ID')
            id_.pack(padx = 10,pady = 10)
            time = Entry(t,bd=0,width = 25,font =('time new roman',21))
            time.insert(0,'Time')
            time.pack(padx = 10,pady = 10)
            teamA = Entry(t,bd=0,width = 25,font =('time new roman',21))
            teamA.insert(0,'Team name')
            teamA.pack(padx = 10,pady = 10)
            score = Entry(t,bd=0,width = 25,font =('time new roman',21))
            score.insert(0,'Score')
            score.pack(padx = 10,pady = 10)
            teamB = Entry(t,bd=0,width = 25,font =('time new roman',21))
            teamB.insert(0,'Team name')
            teamB.pack(padx = 10,pady = 10)
            cal = DateEntry(t, width=12,font = 15, background='Green',foreground='white', bd=2,date_pattern='dd/mm/y')
            cal.pack(side = LEFT,padx=10, pady=10)
            add_new_btn = Button(t,bd= 1,text = ' Add new  ',font=('time new roman',15),command = add)
            add_new_btn.pack(side = TOP,padx = 15,pady = 15)
            t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!')
        pass

    def update(self):
        try:
            # self.user_socket.sendall(bytes(UPDATE,'utf8'))
            # self.user_socket.recv(1)
            def check():
                # self.user_socket.sendall(bytes(SEARCH,'utf8'))
                # self.user_socket.sendall(bytes(id_.get(),'utf8'))
                # flag = self.user_socket.recv(1).decode('utf8')
                if flag == '1':
                    time = Label(fr3,width = 8,font = 12,borderwidth = 1,relief = 'solid')
                    time.grid(column = 0,row= 0)
                    teamA = Label(fr3,width = 20,font = 12,borderwidth = 1,relief = 'solid')
                    teamA.grid(column = 1,row= 0)
                    teamB = Label(fr3,width = 20,font = 12,borderwidth = 1,relief = 'solid')
                    teamB.grid(column = 2,row= 0)

                    # nhan time
                    text = self.user_socket.recv(2048).decode('utf8')
                    self.user_socket.sendall(bytes('1','utf8'))
                    time.configure(text = text)

                    # nhan ten doi 1
                    teamA_name = self.user_socket.recv(2048).decode('utf8')
                    self.user_socket.sendall(bytes('1','utf8'))
                    teamA.configure(text = teamA_name)

                    # nhan ten doi 2
                    teamB_name = self.user_socket.recv(2048).decode('utf8')
                    self.user_socket.sendall(bytes('1','utf8'))
                    teamB.configure(text = teamB_name)

                    # khoang trong
                    temp = Label(t,width = 48,font = 12)
                    temp.grid(column = 0,row = 1,columnspan = 3)

                    row = 2
                    i = 0
                    event_time = []
                    event_A = []
                    event_B = []
                    while True:
                        # nhan thoi gian xay ra su kien
                        text = self.user_socket.recv(2048).decode('utf8')
                        self.user_socket.sendall(bytes('1','utf8'))
                        if text == '_END_':
                            break
                        # nhan ten doi co su kien
                        event_team = self.user_socket.recv(2048).decode('utf8')
                        self.user_socket.sendall(bytes('1','utf8'))
                        # nhan ten su kien
                        event_ = self.user_socket.recv(2048).decode('utf8')
                        self.user_socket.sendall(bytes('1','utf8'))

                        event_time[i] = Label(fr3,width=8,font=12,borderwidth = 1,relief = 'groove')
                        event_time[i].grid(column = 0,row = row)
                        event_time[i].configure(text = text)

                        event_A[i] = Label(fr3,width = 20,font = 12,borderwidth = 1,relief = 'groove')
                        event_A[i].grid(column = 1,row = row)
                        event_B[i] = Label(fr3,width = 20,font = 12,borderwidth = 1,relief = 'groove')
                        event_B[i].grid(column = 2,row = row)

                        if event_team == teamA_name:
                            event_A[i].configure(text = event_)
                        elif event_team == teamB_name:
                            event_B[i].configure(text = event_)
                        i = i + 1
                        row = row + 1
                elif flag == '0':
                    messagebox.showwarning('Search','Cant find that id')
                pass
            def update_score():
                def send_score():
                    self.user_socket.sendall(bytes(id_input.get(),'utf8'))
                    if self.user_socket.recv(1).decode('utf8'):
                        messagebox.showinfo('Update','Success!')
                    else:
                        messagebox.showinfo('Update','Failed!')
                    pass
                s = Toplevel()
                s.grab_set()
                id_input = Entry(s,bd=3,width = 25)
                id_input.insert(0,"Input new score")
                id_input.pack(side=LEFT, padx=10,pady=10)
                k = Button(s,text='Update',command=send_score)
                k.pack(side=LEFT, padx=10,pady=10)
                s.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(s))
                pass
            def udate_time():
                def send_time():
                    self.user_socket.sendall(bytes(id_input.get(),'utf8'))
                    if self.user_socket.recv(1).decode('utf8'):
                        messagebox.showinfo('Update','Success!')
                    else:
                        messagebox.showinfo('Update','Failed!')
                    pass
                s = Toplevel()
                s.grab_set()
                id_input = Entry(s,bd=3,width = 25)
                id_input.insert(0,"Input new time")
                id_input.pack(side=LEFT, padx=10,pady=10)
                k = Button(s,text='Update',command=send_time)
                k.pack(side=LEFT, padx=10,pady=10)
                s.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(s))
                pass
            def update_event():
                def send_event():
                    self.user_socket.sendall(bytes(id_input.get(),'utf8'))
                    if self.user_socket.recv(1).decode('utf8'):
                        messagebox.showinfo('Update','Success!')
                    else:
                        messagebox.showinfo('Update','Failed!')
                    pass
                s = Toplevel()
                s.grab_set()
                id_input = Entry(s,bd=3,width = 25)
                id_input.insert(0,"Input new event")
                id_input.pack(side=LEFT, padx=10,pady=10)
                k = Button(s,text='Update',command=send_event)
                k.pack(side=LEFT, padx=10,pady=10)
                s.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(s))
                pass
            t = Toplevel()
            t.grab_set()

            fr1 = Frame(t)
            fr1.pack()

            fr2 = Frame(t)
            fr2.pack()
            
            fr3 = Frame(t)
            fr3.pack()

            id_ = Entry(fr1,bd=3,width = 25)
            id_.insert(0,'Score ID')
            id_.pack(side = LEFT)
            check_btn = Button(fr1,text = "Check",bd=3,width = 10,command=check)
            check_btn.pack(side = LEFT)

            score_btn = Button(fr2,text = "Update score",bd=3,width = 10,command=update_score)
            score_btn.pack(side = LEFT)
            time_btn = Button(fr2,text = "Update time",bd=3,width = 10,command=udate_time)
            time_btn.pack(side = LEFT)
            event_btn = Button(fr2,text = "Update event",bd=3,width = 10,command=update_event)
            event_btn.pack(side = LEFT)
            t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!') 
        pass

    def reload(self):
        pass

    def refresh(self):
        try:
            self.user_socket.sendall(bytes(REFRESH,'utf8'))
            self.user_socket.recv(1).decode('utf8')

            y = self.cal.get_date().year
            m = self.cal.get_date().month
            d = self.cal.get_date().day
            self.user_socket.sendall(bytes(y,'utf8'))
            self.user_socket.recv(1)
            self.user_socket.sendall(bytes(m,'utf8'))
            self.user_socket.recv(1)
            self.user_socket.sendall(bytes(m,'utf8'))
            self.user_socket.recv(1)
            for i in self.list_all.get_children():
                self.list_all.delete(i)
            while True:
                id_ = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                if id_ == '_END_':
                    break
                time = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamA = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                score = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamB = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                date = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                self.list_all.insert('', 'end' ,value = (id_,time,teamA,score,teamB,date))
            
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!') 

    def detail_dialog(self):
        t = Toplevel()
        t.grab_set()

        time = Label(t,width = 8,font = 12,borderwidth = 1,relief = 'solid')
        time.grid(column = 0,row= 0)
        teamA = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'solid')
        teamA.grid(column = 1,row= 0)
        teamB = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'solid')
        teamB.grid(column = 2,row= 0)

        # nhan time
        text = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        time.configure(text = text)

        # nhan ten doi 1
        teamA_name = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        teamA.configure(text = teamA_name)

        # nhan ten doi 2
        teamB_name = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        teamB.configure(text = teamB_name)

        # khoang trong
        temp = Label(t,width = 48,font = 12)
        temp.grid(column = 0,row = 1,columnspan = 3)

        row = 2
        i = 0
        event_time = []
        event_A = []
        event_B = []
        while True:
            # nhan thoi gian xay ra su kien
            text = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))
            if text == '_END_':
                break
            # nhan ten doi co su kien
            event_team = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))
            # nhan ten su kien
            event_ = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))

            event_time[i] = Label(t,width=8,font=12,borderwidth = 1,relief = 'groove')
            event_time[i].grid(column = 0,row = row)
            event_time[i].configure(text = text)

            event_A[i] = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'groove')
            event_A[i].grid(column = 1,row = row)
            event_B[i] = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'groove')
            event_B[i].grid(column = 2,row = row)

            if event_team == teamA_name:
                event_A[i].configure(text = event_)
            elif event_team == teamB_name:
                event_B[i].configure(text = event_)
            i = i + 1
            row = row + 1


        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def search(self):
        score_id = self.score_id_input.get()
        print(score_id)
        if score_id != '':
            try:
                self.user_socket.sendall(bytes(SEARCH,'utf8'))
                self.user_socket.sendall(bytes(score_id,'utf8'))
                flag = self.user_socket.recv(1).decode('utf8')
                if flag == '1':
                    self.detail_dialog()
                elif flag == '0':
                    messagebox.showwarning('Search','Cant find that id')
            except Exception as e:
                print(e)
                messagebox.showwarning('System','Something went wrong!')                    
        pass

    def logout(self):
        self.grab_release()
        self.destroy()
        self.master.deiconify()
        self.master.grab_set()
        pass

    def predate(self):
        d = None
        try:
            d = datetime(self.cal.get_date().year,self.cal.get_date().month,self.cal.get_date().day - 1)
        except:
            if self.cal.get_date().month == 1:
                d = datetime(self.cal.get_date().year-1,12,31)
            else:
                temp = monthrange(self.cal.get_date().year,self.cal.get_date().month-1)[1]
                d = datetime(self.cal.get_date().year,self.cal.get_date().month-1,temp)
        self.cal.set_date(d)
        pass

    def nextdate(self):
        d = None
        dd = self.cal.get_date().day
        mm = self.cal.get_date().month
        y = self.cal.get_date().year
        if dd == monthrange(y,mm)[1]:
            dd = 1
            if self.cal.get_date().month == 12:
                mm = 1
                y = y + 1
            else:
                mm = mm + 1
        else:
            dd = dd + 1
        d = datetime(y,mm,dd)
        self.cal.set_date(d)
        pass

    def on_closing(self):
        self.master.master.destroy()

    def run(self):
        self.mainloop()
class Client(Toplevel):
    def __init__(self,user_socket,master = None):
        super().__init__(master)
        self.master = master
        self.user_socket = user_socket

        self.master.withdraw()
        self.grab_set()
        self.title('Live Score')
        self.iconbitmap('icon.ico')
        self.geometry("850x650+250+50")
        self.configure(background = 'SeaGreen')
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        img = PhotoImage(file = 'logout.png')
        logout_img = img.subsample(2,2)
        self.logout_btn = Button(self,text = 'LOGOUT',bd=1,width = 80,height = 30,image = logout_img,compound = LEFT,command = self.logout)
        self.logout_btn.image = logout_img
        self.logout_btn.pack(side = TOP,anchor = NE,padx = 5,pady = 5)

        self.fr = Frame(self,bg  = 'LimeGreen')
        self.fr.pack(side = TOP,pady = 10,fill = BOTH)

        self.fr1 = Frame(self.fr,bg  = 'LimeGreen')
        self.fr1.pack()

        self.l = Label(self.fr1,text = 'Score ID: ',fg = 'LightBlue',bg = 'white',bd=0,font = ('time new roman',20))
        self.l.pack(side = LEFT)

        self.score_id_input = Entry(self.fr1,bd=0,width = 25,font =('time new roman',21))
        self.score_id_input.pack(side = LEFT)

        img = PhotoImage(file = 'search.png')
        search_img = img.subsample(1,1)
        self.search_btn = Button(self.fr1,bd = 1,image = search_img,compound = LEFT, command = self.search)
        self.search_btn.image = search_img
        self.search_btn.pack(side = LEFT)

        self.fr2 = Frame(self.fr,bg  = 'LimeGreen')
        self.fr2.pack(pady = 10,padx = 20)

        img = PhotoImage(file = 'previous.png')
        previous_img = img.subsample(2,2)
        self.previous_btn = Button(self.fr2,bd = 1,image = previous_img,compound = LEFT,command = self.predate)
        self.previous_btn.image = previous_img
        self.previous_btn.pack(side = LEFT)
        
        self.cal = DateEntry(self.fr2, width=12,font = 15, background='Green',foreground='white', bd=2,date_pattern='dd/mm/y')
        self.cal.pack(side = LEFT,padx=10, pady=10)

        img = PhotoImage(file = 'next.png')
        next_img = img.subsample(2,2)
        self.next_btn = Button(self.fr2,bd = 1,image = next_img,compound = LEFT,command = self.nextdate)
        self.next_btn.image = next_img
        self.next_btn.pack(side = LEFT)

        img = PhotoImage(file = 'refresh.png')
        refresh_img = img.subsample(2,2)
        self.refresh_btn = Button(self.fr2,bd = 1,image = refresh_img,compound = LEFT,command = self.refresh)
        self.refresh_btn.image = refresh_img
        self.refresh_btn.pack(side = LEFT,padx = 5)

        self.fr3 = Frame(self.fr,bg = 'LimeGreen')
        self.fr3.pack()

        self.list_all = ttk.Treeview(self.fr3,selectmode = 'browse',height = 20)
        self.list_all.pack(side= LEFT)

        self.scoll = ttk.Scrollbar(self.fr3,orient='vertical',command = self.list_all.yview)
        self.scoll.pack(side = 'left',fill='y')

        self.list_all.configure(yscrollcommand = self.scoll.set)

        self.list_all['columns'] = ("1","2","3","4","5","6")
        self.list_all['show'] = 'headings'
        self.list_all.column("1",width = 50,anchor = 'c')
        self.list_all.column("2",width = 50,anchor = 'c')
        self.list_all.column("3",width = 150,anchor = 'c')
        self.list_all.column("4",width = 50,anchor = 'c')
        self.list_all.column("5",width = 150,anchor = 'c')
        self.list_all.column("6",width = 100,anchor = 'c')

        self.list_all.heading("1",text = "ID")
        self.list_all.heading("2",text = "Time")
        self.list_all.heading("3",text = "Team 1")
        self.list_all.heading("4",text = "Ti so")
        self.list_all.heading("5",text = "Team 2")
        self.list_all.heading("6",text = "Date")

        self.list_all_btn = Button(self,bd= 1,text = 'List All',font=('time new roman',15),command = self.listAll)
        self.list_all_btn.pack(side = TOP)

        self.list_all.insert('', -1,value = ('CL11','FT','Chelsea','1 - 1','Real Madrid','28/04/2021'))
        self.list_all.insert('',-1,value = ('CL11','89\'','Liverpool','1 - 1','Barcelona','28/04/2021'))
        self.list_all.insert('', -1 ,value = ('CL11','HT','Chelsea','1 - 1','Arsenal','28/04/2021'))
        pass


    def logout(self):
        self.grab_release()
        self.destroy()
        self.master.deiconify()
        self.master.grab_set()
        pass

    def listAll(self):
        try:
            self.user_socket.sendall(bytes(LISTALL,'utf8'))
            self.user_socket.recv(1).decode('utf8')

            for i in self.list_all.get_children():
                self.list_all.delete(i)
            while True:
                id_ = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                if id_ == '_END_':
                    break
                time = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamA = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                score = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamB = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                date = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                self.list_all.insert('', 'end' ,value = (id_,time,teamA,score,teamB,date))
            
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!')

    def refresh(self):
        try:
            self.user_socket.sendall(bytes(REFRESH,'utf8'))
           # self.user_socket.recv(1).decode('utf8')

            y = str(self.cal.get_date().year)
            m = str(self.cal.get_date().month)
            d = str(self.cal.get_date().day)

            if (len(m) == 1):
            	m = "0" + m
            if (len(d) == 1):
            	d = "0" + d

            date_ = y + "/" + m + "/" + d
            #send Date
            self.user_socket.sendall(bytes(date_,'utf8'))
            self.user_socket.recv(1)


            for i in self.list_all.get_children():
                self.list_all.delete(i)
            while True:
                id_ = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                if id_ == '_END_':
                    break
                time = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamA = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                score = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                teamB = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                date = self.user_socket.recv(1024).decode('utf8')
                self.user_socket.sendall(bytes('1','utf8'))
                self.list_all.insert('', 'end' ,value = (id_,time,teamA,score,teamB,date))
            
        except Exception as e:
            print(e)
            messagebox.showwarning('System','Something went wrong!') 

    def detail_dialog(self):
        t = Toplevel()
        t.grab_set()

        time = Label(t,width = 8,font = 12,borderwidth = 1,relief = 'solid')
        time.grid(column = 0,row= 0)
        teamA = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'solid')
        teamA.grid(column = 1,row= 0)
        teamB = Label(t,width = 20,font = 12,borderwidth = 1,relief = 'solid')
        teamB.grid(column = 2,row= 0)

        # nhan time
        text = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        time.configure(text = text)

        # nhan ten doi 1
        teamA_name = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        teamA.configure(text = teamA_name)

        # nhan ten doi 2
        teamB_name = self.user_socket.recv(2048).decode('utf8')
        self.user_socket.sendall(bytes('1','utf8'))
        teamB.configure(text = teamB_name)

        print( text + "  " + teamA_name + "  " + teamB_name)
        # khoang trong
        temp = Label(t,width = 48,font = 12)
        temp.grid(column = 0,row = 1,columnspan = 3)

        row = 2
        i = 0
        event_time = []
        event_A = []
        event_B = []
        while True:
            # nhan thoi gian xay ra su kien
            text = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))
            if text == '_END_':
                break
            # nhan ten doi co su kien
            event_team = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))
            # nhan ten su kien
            event_ = self.user_socket.recv(2048).decode('utf8')
            self.user_socket.sendall(bytes('1','utf8'))

            print(text + "  " + event_team +  "  " + event_)

            event_time.append(Label(t,width=8,font=12,borderwidth = 1,relief = 'groove'))
            event_time[i].grid(column = 0,row = row)
            event_time[i].configure(text = text)

            event_A.append(Label(t,width = 20,font = 12,borderwidth = 1,relief = 'groove'))
            event_A[i].grid(column = 1,row = row)
            event_B.append(Label(t,width = 20,font = 12,borderwidth = 1,relief = 'groove'))
            event_B[i].grid(column = 2,row = row)

            if event_team == teamA_name:
                event_A[i].configure(text = event_)
            elif event_team == teamB_name:
                event_B[i].configure(text = event_)
            i = i + 1
            row = row + 1

        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def search(self):
        score_id = self.score_id_input.get()
        print(score_id)
        if score_id != '':
        	self.user_socket.sendall(bytes(SEARCH,'utf8'))
        	self.user_socket.sendall(bytes(score_id,'utf8'))
        	self.user_socket.recv(1)
        	flag = self.user_socket.recv(1).decode('utf8')
        	self.user_socket.sendall(bytes("1", "utf8"))
        	print("Flag:" + flag)
        	if flag == '1':
        		self.detail_dialog()
        	elif flag == '0':
        		messagebox.showwarning('Search','Cant find that id')
            # try:
                # self.user_socket.sendall(bytes(SEARCH,'utf8'))

                # self.user_socket.sendall(bytes(score_id,'utf8'))
                # self.user_socket.recv(1)

                # flag = self.user_socket.recv(1).decode('utf8')
                # self.user_socket.sendall(bytes("1", "utf8"))

                # print("Flag:" + flag)
                # if flag == '1':
                #     self.detail_dialog()
                # elif flag == '0':
                #     messagebox.showwarning('Search','Cant find that id')
            # except Exception as e:
            #     print(e)
            #     messagebox.showwarning('System','Something went wrong!')                    
        pass

    def predate(self):
        d = None
        try:
            d = datetime(self.cal.get_date().year,self.cal.get_date().month,self.cal.get_date().day - 1)
        except:
            if self.cal.get_date().month == 1:
                d = datetime(self.cal.get_date().year-1,12,31)
            else:
                temp = monthrange(self.cal.get_date().year,self.cal.get_date().month-1)[1]
                d = datetime(self.cal.get_date().year,self.cal.get_date().month-1,temp)
        self.cal.set_date(d)
        pass

    def nextdate(self):
        d = None
        dd = self.cal.get_date().day
        mm = self.cal.get_date().month
        y = self.cal.get_date().year
        if dd == monthrange(y,mm)[1]:
            dd = 1
            if self.cal.get_date().month == 12:
                mm = 1
                y = y + 1
            else:
                mm = mm + 1
        else:
            dd = dd + 1
        d = datetime(y,mm,dd)
        self.cal.set_date(d)
        pass

    def on_closing(self,func = None):
        if func == None:
            self.master.master.destroy()
        else:
            func.grab_release()
            self.grab_set()
            func.destroy()
        pass

    def run(self):
        self.mainloop()
        pass

class Signup(Toplevel):
    def __init__(self, user_socket, master = None):
        super().__init__(master)
        self.user_socket = user_socket
        self.master = master

        #=============window set up===============
        self.grab_set()
        self.title("SIGN UP")
        self.iconbitmap('icon.ico')
        self.geometry("350x400+350+220")
        self.configure(background='AliceBlue')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False,False)

        #=============create frame===============        
        self.sup = Frame(self,bg='AliceBlue')
        self.sup.pack(side = LEFT)

        self.frame1 = Frame(self.sup,bg='AliceBlue')
        self.frame1.pack(padx=40,anchor=CENTER)

        self.frame2 = Frame(self.sup,bg='AliceBlue')
        self.frame2.pack(padx=40,pady=10)

        self.frame3 = Frame(self.sup,bg='AliceBlue')
        self.frame3.pack(padx=40, pady=10)

        self.frame4 = Frame(self.sup,bg='AliceBlue')
        self.frame4.pack(pady=15)

        #=============create input===============
        self.username_img = PhotoImage(file='user_img.png')
        self.username_label = Label(self.frame1,image=self.username_img,bg='AliceBlue').grid(column=0,row=0)
        self.user_input = Entry(self.frame1,bd=6,font=15,fg='grey')
        self.user_input.insert(0, "Username")
        self.user_input.bind("<FocusIn>", self.foc_in)
        self.user_input.grid(column=1,row=0,padx=15,pady=10)

        self.password_img = PhotoImage(file='pass_img.png')
        self.password_label = Label(self.frame2,image=self.password_img,bg='AliceBlue').grid(column=0,row=0)
        self.pass_input = Entry(self.frame2,fg='grey',bd=6,font=15)
        self.pass_input.insert(0, "Password")
        self.pass_input.bind("<FocusIn>", self.foc_in)
        self.pass_input.grid(column=1,row=0,padx=15)

        self.con_password_label = Label(self.frame3,image=self.password_img,bg='AliceBlue').grid(column=0,row=0)
        self.con_pass_input = Entry(self.frame3,fg='grey',bd=6,font=15 )
        self.con_pass_input.insert(0, "Confirm Password")
        self.con_pass_input.bind("<FocusIn>", self.foc_in)
        self.con_pass_input.grid(column=1,row=0,padx=10)

        #=============create button===============
        self.signup_btn = Button(self.frame4,text='SIGN UP',width=33,font=("time new roman",10),command=self.signup)
        self.signup_btn.pack(anchor = 'ne',padx = 6)
        pass

    def foc_in(self,event):
        if event.widget == self.user_input:
            if self.user_input['fg'] == 'grey':
                self.user_input['fg'] ='black'
                self.user_input.delete('0', 'end')
        elif event.widget == self.pass_input:
            if self.pass_input['fg'] == 'grey':
                self.pass_input['fg'] ='black'
                self.pass_input['show'] ='*'
                self.pass_input.delete('0', 'end')
        elif event.widget == self.con_pass_input:
            if self.con_pass_input['fg'] == 'grey':
                self.con_pass_input['fg'] ='black'
                self.pass_input['show'] ='*'
                self.con_pass_input.delete('0', 'end')
        pass

    def signup(self):
        self.focus()
        username = self.user_input.get()
        password = self.pass_input.get()
        confirm_password = self.con_pass_input.get()
        print(username)
        print(password)
        print(confirm_password)

        if username != "" and password != "" and confirm_password != "":
            if password.lower() == confirm_password.lower():
                try:
                    self.user_socket.sendall(bytes(REGISTER,'utf8'))
                                       
                    self.user_socket.sendall(bytes(username,'utf8'))
                    #check username already exist
                    flag = self.user_socket.recv(1).decode('utf8')

                    # flag = 0 mean usernname is not exist
                    if flag == '0':
                        self.user_socket.send(bytes(password,'utf8'))
                        messagebox.showinfo("Sign up","Success!\nYour account has been created")
                    # flag = 1 mean username was exist
                    elif flag == '1':
                        messagebox.showerror("Sign up","Account already exists")
                except:
                    messagebox.showwarning("Warning","Oops!\nSomething went wrong.")
            else:
                messagebox.showerror("Sign up","Password are not matching")
        pass   

    def on_closing(self):
        self.grab_release()
        if self.master != None:
            self.master.grab_set()
        self.destroy()
        pass

    def run(self):
        self.mainloop()
        pass 

class Login(Toplevel):
    def __init__(self, user_socket, master = None):
        super().__init__(master)
        self.master = master
        self.grab_set()

        #====================== WINDOW SET UP ======================
        self.user_socket = user_socket
        self.title("LOGIN")
        self.iconbitmap('icon.ico')
        self.geometry("950x400+300+200")
        self.configure(background='AliceBlue')
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        bg_img = Image.open('background.png')
        cre_bg_img = bg_img.resize((600,400),Image.ANTIALIAS)
        render_img = ImageTk.PhotoImage(cre_bg_img)
        self.background = Label(self,image=render_img)
        self.background.image = render_img
        self.background.pack(side = LEFT)


        #====================== LOGIN FORM ======================
        self.fr1 = Frame(self,bg='AliceBlue')
        self.fr1.pack(side = LEFT,fill = BOTH,pady = 80)

        self.frame1 = Frame(self.fr1,bg='AliceBlue')
        self.frame1.pack(padx=40)

        self.frame2 = Frame(self.fr1,bg='AliceBlue')
        self.frame2.pack(padx=40,pady=5)

        self.frame3 = Frame(self.fr1,bg='AliceBlue')
        self.frame3.pack(padx=40, pady=5)

        self.username_img = PhotoImage(file='user_img.png')
        self.username_label = Label(self.frame1,image=self.username_img,bg='AliceBlue').grid(column=0,row=0)
        self.user_input = Entry(self.frame1,bd=6,font=15,fg='grey')
        self.user_input.insert(0, "Username")
        self.user_input.bind("<FocusIn>", self.foc_in)
        self.user_input.grid(column=1,row=0,padx=10,pady=10)

        self.password_img = PhotoImage(file='pass_img.png')
        self.password_label = Label(self.frame2,image=self.password_img,bg='AliceBlue').grid(column=0,row=0)
        self.pass_input = Entry(self.frame2,fg='grey',bd=6,font=15)
        self.pass_input.insert(0, "Password")
        self.pass_input.bind("<FocusIn>", self.foc_in)
        self.pass_input.grid(column=1,row=0,padx=10)

        self.login_btn = Button(self.frame3,text=' L O G I N ',width=28,bd = 1,fg = 'blue',font=("time new roman",10),command=self.login)
        self.login_btn.pack(anchor = CENTER)

        self.label1 = Label(self.frame3, text="       Don't have an account?  ",font=("time new roman",12),height=2,bd=1)
        self.label1.pack(side=LEFT,pady=35)

        self.signup_btn = Button(self.frame3,text='  SIGN UP    ',font=("time new roman",10),height=2,bd=0,fg='blue',command=self.signup)
        self.signup_btn.pack(side=RIGHT)
        pass

    def foc_in(self, event):
        if event.widget == self.user_input:
            if self.user_input['fg'] == 'grey':
                self.user_input['fg'] ='black'
                self.user_input.delete('0', 'end')
        elif event.widget == self.pass_input:
            if self.pass_input['fg'] == 'grey':
                self.pass_input['fg'] ='black'
                self.pass_input['show'] ='*'
                self.pass_input.delete('0', 'end')
        pass

    def login(self):
        # Viewapp = Admin(self.user_socket,self)
        # # Viewapp = Client(self.user_socket,self)
        # Viewapp.run() 
        
        username = self.user_input.get()
        password = self.pass_input.get()
        self.focus()
        flag = ''
        if username != "" or password != "":
            try:       
                self.user_socket.sendall(bytes(LOGIN,'utf8'))

                self.user_socket.sendall(bytes(username,'utf8'))
                flag = self.user_socket.recv(100)

                self.user_socket.sendall(bytes(password,'utf8'))
                flag = self.user_socket.recv(1).decode('utf8')

                print(flag)
            except:
                messagebox.showwarning("Warning","Oops!\nSomething went wrong.")

            Viewapp = None
            #No account
            if flag == '3':
                messagebox.showerror()("Login failed","Incorrect username or password.\nPlease try again.")
                self.role = -1
            elif flag == "2":
                messagebox.showwarning("Warning","Your account login from another device!")
            #Admin
            elif flag == '1':
                self.role = 1
                Viewapp = Admin(self.user_socket,self)
                Viewapp.run()                 
            #Client
            elif flag == '0':
                self.role = 0
                Viewapp = Client(self.user_socket,self)
                Viewapp.run()
            
            # if Viewapp != None:
            #     View.run()
        pass

    def signup(self):
        s = Signup(self.user_socket,self)
        s.run()
        pass

    def on_closing(self):
        self.grab_release()
        self.destroy()
        self.master.deiconify()
        pass

    def run(self):
        self.mainloop()
        pass

class App(Tk):
    def __init__(self):
        super().__init__()
        self.client_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.title('Live Score - Check Connection')
        self.iconbitmap('icon.ico')
        self.configure(background = 'PaleGreen')
        self.geometry('400x200+600+300')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(0,0)
        
        self.fr1 = Frame(self,bg = 'PaleGreen')
        self.fr1.pack(fill = BOTH, ipadx = 50,pady = 50)

        self.input_ip = Entry(self.fr1,bd = 3,fg = 'red',font = ("time new roman",12))
        self.input_ip.insert(0,'127.0.0.1')
        self.input_ip.pack(pady = 5)

        self.conn_btn = Button(self.fr1,text= 'Connect',fg='Red',font=('time new roman',12),bd = 3, width = 20,height= 3,justify = CENTER,command = self.connect)
        self.conn_btn.pack(pady = 5)

        pass

    def connect(self):
        ip = self.input_ip.get()
        server_address = (ip,PORT)
        try:
            self.client_connect.connect(server_address)
            self.process()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",'Cant connect to server.\nCheck your connection and try again.')
        pass

    def process(self):
        self.withdraw()
        Viewapp = Login(self.client_connect,self)
        Viewapp.run()
        pass

    def on_closing(self):
        self.destroy()
        pass
    
    def run(self):
        self.mainloop()
        pass

if __name__ == "__main__":
    myApp = App()
    myApp.run()
