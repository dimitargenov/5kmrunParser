from html.parser import HTMLParser
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import MySQLdb
from MainConfig import config
import re

class HTMLParser(HTMLParser):
	def connectDb(self):
		self.db = MySQLdb.connect(host=config['host'],  # your host 
                     user=config['username'],       # username
                     passwd=config['password'],     # password
                     db=config['database'],
                     use_unicode=config['use_unicode'],
                     charset=config['charset'])   # name of the database
		self.cursor = self.db.cursor()

	def __init__(self, url):
		self.domain = domain

	def getTimeInSeconds(self, time):
		if (len(time) == 5):
			time = "00:" + time
			
		return sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))

	def getHtmlContent(self, url: str):
		fp = urllib.request.urlopen(url)
		htmlAsBytes = fp.read()
		html = htmlAsBytes.decode("utf8")
		fp.close()

		return html

	def getDomParkId(self, domPark):
		return {
        	'Южен Парк': 1,
        	'Западен Парк': 2,
        	'Морска градина (Варна)': 3,
        	'Парк Лаута (Пловдив)': 4,
        	'Морска градина (Бургас)': 5,
        	'Южен парк 2': 6,	
        	'Бялата Порта (Самоков)': 7,
        	'Гребен канал 2 (Пловдив)': 8,
        	'НДК - Южен Парк 5 км.': 9,
        	'Разград': 10,
        	'Борисова градина (София)': 11,
        	'Морска градина2 (Бургас)': 12,
        	'София Екиден Маратон': 14,
        	'Брюксел (София)': 13,
        	'Западен парк 2': 15
    	}[domPark]

	def extractRaceData(self, text):
		raceData = {}
		domPark = re.search(r'-\s(.*?)\)$', text).group(1)
		date = re.search(r'\((.*?)\s-', text).group(1)
		raceData['domParkId'] = self.getDomParkId(domPark)
		raceData['raceDate'] = datetime.strptime(date, '%d.%m.%Y').strftime('%Y/%m/%d')
		raceData['name'] = text
		
		return raceData	

	def insertResultInDb(self,runnerData,raceId):
		self.connectDb()
		try:
			timeInSeconds = self.getTimeInSeconds(runnerData[3].text)
			
			if (runnerData[1].text == 'Няма'):
				runnerId = 0
				sexPosition = 0
				agePosition = 0
				points = 0
				totalRuns = 0
				agePercent = 0
			else:
				runnerId = runnerData[1].text	
				sexPosition = runnerData[6].text
				agePosition = runnerData[7].text
				points = runnerData[9].text
				totalRuns = runnerData[11].text
				agePercent = runnerData[8].text[:-1]
			
			query = "INSERT INTO Results (" \
				"Position,RunnerId,Name, `Time`,Age,Sex, SexPosition,AgePosition,Points, TotalRuns,TimeInSeconds,AgePercent, RaceId)" \
				"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			args = (runnerData[0].text,runnerId,runnerData[2].text, runnerData[3].text,runnerData[4].text,runnerData[5].text,
					sexPosition,agePosition,points, totalRuns,timeInSeconds,agePercent,raceId)

			self.cursor.execute(query, args)
			timeInSeconds = self.getTimeInSeconds(runnerData[3].text)
			res = self.db.commit()
			if (res == None and runnerData[1].text != 'Няма' and (self.runnerExists(runnerId) == False)):
				self.insertRunner(runnerId, runnerData[2].text, runnerData[4].text, runnerData[5].text)
			print(runnerId, res)
		   	
		except Exception as e:
			self.db.rollback()
			print(str(e))
			exit(2)

	def runnerExists(self, runnerId):
		self.connectDb()
		self.cursor.execute("SELECT Id FROM Runner WHERE RunnerId = {0}".format(runnerId))
		if (self.cursor.rowcount != 0):
			return True
		else:
			return False	

	def insertRunner(self, runnerId, name, age, sex):
		self.connectDb()
		try:
			if (sex == 'Мъж'):
				sex = 1
			else:
				sex = 2

			query = "INSERT INTO Runner (RunnerId,Name,AgeCategory,Sex)" \
					"VALUES (%s,%s,%s,%s)"
			args = (runnerId,name,age,sex)

			self.cursor.execute(query, args)
			res = self.db.commit()
		except Exception as e:
			self.db.rollback()
			print(str(e))
			exit(1)			

	def insertRaceInDb(self,raceData):
		self.connectDb()
		try:
			query = "INSERT INTO Race (EventId,DomParkId,Name,Date)" \
					"VALUES (%s,%s,%s,%s)"
			args = (raceData['eventId'],raceData['domParkId'],raceData['name'],raceData['raceDate'])

			self.cursor.execute(query, args)
			res = self.db.commit()
		except Exception as e:
			self.db.rollback()
			print(str(e))
			exit(1)

		return self.cursor.lastrowid

	def process(self, url, eventId):
		resultUrl = self.domain + '/' + url
		html = self.getHtmlContent(resultUrl)
		soup = BeautifulSoup(html, 'html.parser')
		race = soup.find('div', {'class': 'col-sm-12'}).findAll('h3')
		if race[0].text.find("1970") != -1:
			return False
		raceData = self.extractRaceData(race[0].text)
		raceData['eventId'] = eventId
		print('-----Inserting Event---------' + str(eventId))
		raceId = self.insertRaceInDb(raceData)
		results = soup.find('table', {'class': 'table-bordered'}).findAll('tr')
		for row in results[1:]:
			runnerData = row.findAll('td')
			self.insertResultInDb(runnerData, raceId)

	def eventExists(self, eventId):
		self.connectDb()
		self.cursor.execute("SELECT Id FROM Race WHERE EventId = {0}".format(eventId))
		if (self.cursor.rowcount != 0):
			return True
		else:
			return False

	def getAndParseEventUrls(self, eventsPageUrl):
		html = self.getHtmlContent(eventsPageUrl)	
		soup = BeautifulSoup(html, 'html.parser')
		events = soup.findAll('a', {'class': 'cal_ev'})
		counter = 0
		for event in reversed(events):
			if (counter == 50):
			 	print(counter)
			 	break;
			eventId = int(re.search(r'event=(.*?)&', event.get('href')).group(1))
			if (not self.eventExists(eventId)):
				self.process(event.get('href'), eventId)
				counter+=1
			
domain = 'http://5km.5kmrun.bg'
parser = HTMLParser(domain)
parser.getAndParseEventUrls('http://5km.5kmrun.bg/calendar-a.php')
