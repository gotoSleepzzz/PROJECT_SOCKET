import sqlite3


conn = sqlite3.connect('DATABASE.db')

c = conn.cursor()







# # date = '2021/4/29'
# c.execute("select * from EVENT_MATCH ")


# for i in c:
# 	print(i[0] + "  " + i[1] + "  " + i[2] + "  " + i[3] )


# 	break
# s = 3

# print(len(str(s)))

# #____________________MATCH___________________________
# c.execute("""
# 	CREATE TABLE MATCH
# 	(
# 	ID_MATCH varchar(10) NOT NULL,
# 	CLUB1 varchar(50),
# 	CLUB2 varchar(50),
# 	SCORE varchar(10),   
# 	DATE_ date,
# 	TIME_SCORE varchar(10),
# 	-- FT: het gio , HT: het hiep 1, 0: chua dien ra, 1: dang dien ra
# 	PRIMARY KEY(ID_MATCH)
# 	)
# """)



c.execute("""
	INSERT INTO EVENT_MATCH (ID_MATCH, CLUB, TIME_, EVENT_)
	VALUES ('224697', ' Dacia Buiucani ', '15', 'Marquinhos - Goal'),
		   ('224697', ' Dacia Buiucani ', '31', 'Joao Cancelo - Yellow Card'),
		   ('224697', ' Dacia Buiucani ', '64', 'Kevin De Bruyne - Goal'),
		   ('224697', ' Dinamo-Auto ', '70', 'Leandro Daniel Paredes - Yellow Card'),
		   ('224697', ' Dinamo-Auto ', '71', 'Riyad Mahrez - Goal')

 """)



# #___________________ACCOUNT________________________________
# c.execute(""" 
# 	CREATE TABLE ACCOUNTS (
# 	USERNAME_ DATATYPE text,
# 	PASSWORD_ text,
# 	ROLE_ text,
# 	STATUS_ integer
# 	)
# """)


# c.execute("""
# 	INSERT INTO ACCOUNTS VALUES('admin', 'admin','Admin',0),
# 							   ('TienTri', '1234', 'Client', 0),
# 							   ('HuuThong', '1234', 'Client', 0)
# """)

# #____________________MATCH___________________________
# c.execute("""
# 	CREATE TABLE MATCH
# 	(
# 	ID_MATCH varchar(10) NOT NULL,
# 	CLUB1 varchar(50),
# 	CLUB2 varchar(50),
# 	SCORE varchar(10),   
# 	DATE_ date,
# 	TIME_SCORE varchar(10),
# 	-- FT: het gio , HT: het hiep 1, 0: chua dien ra, 1: dang dien ra
# 	PRIMARY KEY(ID_MATCH)
# 	)
# """)

#_____________________Event_match_____________________
# c.execute("""
# 	CREATE TABLE EVENT_MATCH(	
# 	ID_MATCH varchar(10),
# 	CLUB varchar(50),
# 	TIME_ varchar(5),
# 	EVENT_ varchar(100)
# 	)
# """)





conn.commit()

conn.close()


