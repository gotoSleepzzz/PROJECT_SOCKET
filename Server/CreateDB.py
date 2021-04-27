import sqlite3

conn = sqlite3.connect('DATABASE1.db')

c = conn.cursor()

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


conn.commit()

conn.close()


