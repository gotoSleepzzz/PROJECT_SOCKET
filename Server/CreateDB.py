import sqlite3


conn = sqlite3.connect('DATABASE.db')

c = conn.cursor()
#___________________ACCOUNT________________________________
c.execute(""" 
	CREATE TABLE ACCOUNTS (
	USERNAME_ DATATYPE text,
	PASSWORD_ text,
	ROLE_ text,
	STATUS_ integer
	)
""")


c.execute("""
	INSERT INTO ACCOUNTS VALUES('admin', 'admin','Admin',0),
							   ('TienTri', '1234', 'Client', 0),
							   ('HuuThong', '1234', 'Client', 0)
""")
#____________________footbal_league________________________
c.execute("""
	CREATE TABLE FOOTBALL_LEAGUE(
	ID	varchar(5) PRIMARY KEY,
	NAME_LEAGUE varchar(50)
	)
""")

#____________________MATCH___________________________
c.execute("""
	CREATE TABLE MATCH
	(
	ID_MATCH varchar(5) NOT NULL,
	ID_LEAGUE varchar(5) NOT NULL,
	CLUB1 varchar(50),
	CLUB2 varchar(50),
	SCORE1 varchar(3),   --- Th1: diem so , --Th2: "?"
	SCORE2 varchar(3),   --- Th1: diem so , --Th2: "?"
	DATE_ date,
	TIME_ time,
	TIME_SCORE varchar(10),
	-- FT: het gio , HT: het hiep 1, 0: chua dien ra, 1: dang dien ra
	STATUS_ varchar(3),
	PRIMARY KEY(ID_MATCH, ID_LEAGUE)
	FOREIGN KEY(ID_LEAGUE) REFERENCES FOOTBALL_LEAGUE(ID)
	)
""")

#_____________________Event_match_____________________
c.execute("""
	CREATE TABLE EVENT_MATCH(	
	ID varchar(5) NOT NULL,
	ID_MATCH varchar(5),
	CLUB varchar(50),
	TIME_ varchar(5),
	NAME_PLAYER varchar(50),
	EVENT_ VARCHAR(2), --0: THẺ VÀNG , 1: THẺ ĐỎ, 2: GOAL
	SCORE VARCHAR(10)
	)
""")



conn.commit()

conn.close()


