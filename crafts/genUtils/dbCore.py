import sqlite3 as sql
import sys


class DB:
	def __init__(self, dbFile = ''):
		self.db = dbFile
		try:
			self.con = sql.connect(self.db)
		except:
			sys.exit("\nFailed to connect database\n")
		self.cur = self.con.cursor()
