import sqlite3


conn = sqlite3.connect('DATABASE.db')

c = conn.cursor()

name = "admin"
password = "admin"

c.execute(
	"select * from ACCOUNTS"
)

for i in c:
	print(i)

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
# 	ID varchar(5) NOT NULL,
# 	ID_MATCH varchar(5),
# 	CLUB varchar(50),
# 	TIME_ varchar(5),
# 	NAME_PLAYER varchar(50),
# 	EVENT_ VARCHAR(2), --0: THẺ VÀNG , 1: THẺ ĐỎ, 2: GOAL
# 	SCORE VARCHAR(10),
# 	PRIMARY KEY(ID)
# 	)
# """)

conn.commit()

conn.close()


