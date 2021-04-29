import sqlite3


conn = sqlite3.connect('DATABASE.db')

c = conn.cursor()

date = '2021/04/29'

c.execute("select * from MATCH where DATE_ = ?", [date])


for i in c:
	print(i[0])
	print(i[1])
	print(i[2])
	print(i[3])
	print(i[4])
	print(i[5])

	break

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



# c.execute("""
# 	INSERT INTO EVENT_MATCH (ID_MATCH, CLUB, TIME_, NAME_PLAYER, EVENT_, SCORE)
# 	VALUES('394826', ' Paris Saint-Germain ', '15', 'Marquinhos', 'Goal', ' 1 - 0 '),
# 		   ('394826', ' Manchester City ', '31', 'Joao Cancelo', 'Yellow', ' 1 - 0 '),
# 		   ('394826', ' Manchester City ', '64', 'Kevin De Bruyne', 'Goal', ' 1 - 1 '),
# 		   ('394826', ' Paris Saint-Germain ', '70', 'Leandro Daniel Paredes', 'Yellow', ' 1 - 0 '),
# 		   ('394826', ' Manchester City ', '71', 'Riyad Mahrez', 'Goal', ' 1 - 2 ')

# """)



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



# #_____________________Event_match_____________________
# c.execute("""
# 	CREATE TABLE EVENT_MATCH(	
# 	ID_MATCH varchar(5),
# 	CLUB varchar(50),
# 	TIME_ varchar(5),
# 	NAME_PLAYER varchar(50),
# 	EVENT_ VARCHAR(2), --0: THẺ VÀNG , 1: THẺ ĐỎ, 2: GOAL
# 	SCORE VARCHAR(10)
# 	)
# """)

conn.commit()

conn.close()


