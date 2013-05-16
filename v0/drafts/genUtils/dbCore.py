import sqlite3 as sql
import sys

DBFILE = '/Users/rainy/Projects/Github/sniky.github.com/drafts/db/sniky.blog.sqlite'

class DB:
	def __init__(self, dbFile = DBFILE):
		self.db = dbFile
		try:
			self.con = sql.connect(self.db)
		except:
			sys.exit("\nFailed to connect database\n")
		self.cur = self.con.cursor()
