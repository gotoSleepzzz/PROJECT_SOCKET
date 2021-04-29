import requests
from bs4 import BeautifulSoup
import sqlite3

class Crawl():
	def __init__(self):
		self.conn = sqlite3.connect('DATABASE.db')
		self.c = self.conn.cursor()
		self.html_text = requests.get('https://www.livescores.com/').text
		self.soup = BeautifulSoup(self.html_text, 'lxml')

	def Run(self):
		R = self.soup.find_all('div', class_='row-gray even')
		for result in R:
		 	id_ = result['data-eid']
		 	date = result['data-esd']
		 	date_ = date[0:4] + "/" + date[4:6] + "/" + date[6:8]
		 	min_ = result.find('div', class_='min').text
		 	club1 = result.find('div', class_='ply tright name').text
		 	club2 = result.find('div', class_= 'ply name').text
		 	r1 = result.find('div', class_='sco')
		 	score = r1.text

	 		try:
	 			self.c.execute("""
				INSERT INTO MATCH(ID_MATCH, CLUB1, CLUB2, SCORE, DATE_, TIME_SCORE) 
				VALUES (?, ?,?,?,?,?)

				""",(str(id_), club1, club2, score, date_, min_)
				)
	 		except:
	 			t = 1
	def Commit(self):
		self.conn.commit()
		self.conn.close()
