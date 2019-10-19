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

	def __init__(self, domain):
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

	def clearText(self, text):
		return text.strip();	

	def extractAndInsertResultInDb(self,runnerData,raceId):
		if (runnerData[1].text.strip() == ''):
			runnerId = 0
			points = 0
			totalRuns = 0
			agePercent = 0
			age = 0
			agePercent = 0
			gender = ''
		else:
			runnerId = int(runnerData[1].text)
			age = self.clearText(runnerData[4].text)
			gender = self.clearText(runnerData[5].text)	
			points = int(runnerData[7].text)
			totalRuns = int(runnerData[9].text)
			agePercent = self.clearText(runnerData[6].text)[:-1]
		
		position = int(runnerData[0].text)
		name = self.clearText(runnerData[2].text)
		time = self.clearText(runnerData[3].text)
		sexPosition = 0
		agePosition = 0
		timeInSeconds = self.getTimeInSeconds(self.clearText(runnerData[3].text))	
		
		args = (position,runnerId,name,time,age,gender,sexPosition,agePosition,points,totalRuns,
			timeInSeconds,agePercent,raceId)
		res = self.insertResults(args)
		if (res == None and runnerId != 0 and (self.runnerExists(runnerId) == False)):
			self.insertRunner(runnerId, name, age, gender)
		print(res)

	def insertResults(self, args):
		self.connectDb()
		try:
			query = "INSERT INTO Results (" \
				"Position,RunnerId,Name,`Time`,Age,Sex,SexPosition,AgePosition,Points,TotalRuns,TimeInSeconds,AgePercent,RaceId)" \
				" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			self.cursor.execute(query, args)
			return self.db.commit()
		   	
		except Exception as e:
			print('FAULT')
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
		html = self.getHtmlContent(url)
		soup = BeautifulSoup(html, 'html.parser')
		race = soup.find('strong', {'class': 'title'})
		if race.text.find("1970") != -1:
			return False
		raceData = self.extractRaceData(race.text)
		raceData['eventId'] = eventId
		print('-----Inserting Event---------' + str(eventId))
		raceId = self.insertRaceInDb(raceData)
		results = soup.find('table', {'id': 'event_table'}).findAll('tr')
		for row in results[1:]:
			runnerData = row.findAll('td')
			#print(runnerData)
			self.extractAndInsertResultInDb(runnerData, raceId)

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
		events = soup.findAll('div', {'class': 'preview'})
		counter = 0
		for event in reversed(events):
			if (counter == 50):
			 	print(counter)
			 	break
			url = event.findAll('a')[0].get('href') 	
			eventId = int(url[-4:])
			if (not self.eventExists(eventId)):
				self.process(url, eventId)
				counter+=1

parser = HTMLParser(config['url'])
parser.getAndParseEventUrls(config['resultsPageUrl'])


# Result https://5kmrun.bg/5kmrun/result/1429
# Calendar https://5kmrun.bg/5kmrun/results