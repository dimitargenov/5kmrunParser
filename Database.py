import MySQLdb
from MainConfig import config

class Database():
	def connectDb(self):
		self.db = MySQLdb.connect(host=config['host'],  # your host 
                     user=config['username'],       # username
                     passwd=config['password'],     # password
                     db=config['database'],
                     use_unicode=config['use_unicode'],
                     charset=config['charset'])   # name of the database
		self.cursor = self.db.cursor()

	def exists(self, tableName, id):
		self.connectDb()
		self.cursor.execute("SELECT Id FROM {0} WHERE RunnerId = {1}".format(tableName,runnerId))
		if (self.cursor.rowcount != 0):
			return True
		else:
			return False

	def insert(self, queryString, tableName, data):
		self.connectDb()
				
			