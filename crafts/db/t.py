import sqlite3 as sql

con = sql.connect('sniky.blog.sqlite')
cur = con.cursor()

cur.execute('SELECT id, title, create_date, cate_name, permalink FROM article WHERE cate_name = "psych" ORDER BY create_date DESC')
res = cur.fetchall()

if len(res) != 0:
	print 123
