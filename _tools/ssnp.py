#!/usr/bin/python
#-*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")


"""
Ssnp is a Script Not a Project

Markdown -> HTML

Article use tag:
<p class="[img]"><a><img><blockquote><pre class="prettyprint"><ul | ol><li><hr><strong><span>
"""

###################################################################################################
#	API(with Template var, DB, Format etc.)
#	===========================================
#	1. article.tpl
#	Var = {
#		title: "TITLE",
#		keywords: "k1, k2, k3",
#		date: "Mmm dd, YYYY",#datetimeStr['article']
#		blogbody: "BODY",
#		prevLink: "PREV_LINK",
#		nextLink: "NEXT_LINK"
#	}
# 	===========================================
#	2. index.tpl
#	Var = {
#		articles = {
#			datetime: "yyyy-mm-dd hh:mm",#datetimeStr['index']
#			date: "dd Mmm yyyy",#datetimeStr['indexD']
#			time: "hh:mm",#datetimeStr['indexT']
#			title: "TITLE",
#			brief: "BRIEF",
#			permalink: "url"
#		}
#	}
#	===========================================
#	3. Database
#	[id, title, create_date, last_update, posted, cate_name, permalink, brief]
###################################################################################################
import sys
import os.path
from jinja2 import Template, FileSystemLoader, Environment
import misaka
import re, yaml
from datetime import datetime
import sqlite3 as sql

#tool functions
def log(logstr):
	print "\n%s\n" % logstr
def Md2HTML(blog):
	log("Translate Md file 2 HTML...")
	return misaka.html(blog)
def Tpl(path = "./", tfile = ""):
	log("Creating Template from file: <%s>" % tfile)
	return Environment(loader = FileSystemLoader("./")).get_template(tfile)
def parseBlogConfigArea(blogstr = ""):
	log("Parsing Blog Config Area")
	reConf = r'(<.*><conf[\s\S]*?>([\s\S]*?)<\/conf><.*>)'
	res = re.match(reConf, blogstr)
	if res is None:
		print 'Confg area not found'
		sys.exit()
	res = re.findall(reConf, blogstr)
	blogInfo = yaml.load(res[0][1])
	return blogInfo
def splitArticleBody(blogstr = ""):
	log("Spliting Blog body from draft")
	reTitle = r"([\s\S]*?)<\/h1>"
	res = re.match(reTitle, blogstr)
	if res is None:
		print "Failed to find Title from draft, using <h1>Title</h1>?"
		sys.exit()
	res = re.findall(reTitle, blogstr)
	return blogstr[len(res[0])+len("</h1>"):]
def articleBrief(htmlStr):
	log("Parsing Blog Brief part")
	reBrief = r'<\/h1>[\s\S]*?<p>([\s\S]*?)<\/p>'
	res = re.match(reBrief, htmlStr)
	if res is None and 0:
		print "Failed to find Brief <p>!"
		sys.exit()
	res = re.findall(reBrief, htmlStr)
	return  res[0]
def processDatetime(dtstr):
	log("Processing timeline")
	timeline = datetime.strptime(dtstr, "%Y%m%d%H%M")
	return {"article": datetime.strftime(timeline, "%b %d, %Y"),
			"index": datetime.strftime(timeline, "%Y-%m-%d %H:%M"),
			"indexD": datetime.strftime(timeline, "%d %b %Y"),
			"indexT": datetime.strftime(timeline, "%H:%M")}
def get_next(aid = 0):
	log("Parsing next_link...")
	cur.execute('SELECT permalink FROM article WHERE id > %s ORDER BY id LIMIT 1' % aid)
	link = cur.fetchone()
	next_link = (link is None) and  'javascript:alert(\'已经是最后一篇！\')' or link[0]
	return next_link
def get_prev(aid = 0):
	log("Parsing prev_link...")
	cur.execute('SELECT permalink FROM article WHERE id < %s ORDER BY id DESC LIMIT 1' % aid)
	link = cur.fetchone()
	prev_link = (link is None) and 'javascript:alert(\'已经是第一篇！\')' or link[0]
	return prev_link

#process workflow
DEBUG = 0
DBF = "./db/sniky.github.io.sqlite"
try:
	log("Connecting to database: <%s>" % DBF)
	con = sql.connect(DBF)
except:
	sys.exit("\nFailed to connect database\n")
cur = con.cursor()

args = sys.argv
draft = args[1]
if os.path.isfile(draft):
	print "Draft file: <%s>" % draft
else:
	print "No such file!"
	sys.exit()

blogFile = open(draft, "r")
mdStr = blogFile.read()
blogFile.close()

htmlStr = Md2HTML(mdStr)
blogInfo = parseBlogConfigArea(htmlStr)
blogBody = splitArticleBody(htmlStr)
blogBrief = articleBrief(htmlStr)

dtstr = blogInfo['datetime'] is None and datetime.strftime(datetime.now(), "%Y%m%d%H%M") or str(blogInfo['datetime'])
datetimeStr = processDatetime(dtstr)
articleTplVar = {
	"title": blogInfo['title'],
	"keywords": blogInfo['tags'],
	"date": datetimeStr['article'],
	"blogbody": blogBody
}

cur.execute("SELECT id FROM article WHERE title = '%s'" % articleTplVar['title'])
res = cur.fetchone()
if res is not None:
	articleID = res[0]
	log("Article #%s# is already exist" % articleTplVar['title'])
else:
	cur.execute("INSERT INTO article(title, create_date, last_update, posted, cate_name, permalink, brief) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (articleTplVar['title'], dtstr, dtstr, 0, "article", blogInfo['permalink'], blogBrief))
	con.commit()
	log("New article #%s# saved" % articleTplVar['title'])

	cur.execute("SELECT id FROM article WHERE title = '%s'" % articleTplVar['title'])
	res = cur.fetchone()
	articleID = res[0]

prev_link = get_prev(articleID)
next_link = get_next(articleID)

tpl = Tpl(tfile="article.tpl")
articleTplVar['prevLink'] = prev_link
articleTplVar['nextLink'] = next_link
output = tpl.render(articleTplVar)

articleFileName = blogInfo['permalink'].split("/")[-1]
articleFile = os.path.join("../article/", articleFileName)

log("Saving article file <%s> to <%s>" % (articleFileName, articleFile))
f = open(articleFile, "w")
f.write(output)
f.close()

log("Update index page")
cur.execute("SELECT title, create_date, brief, permalink, id FROM article ORDER BY create_date DESC")
allArticle = cur.fetchall()
articles = []
for art in allArticle:
	aid = art[4]
	prev_link = get_prev(aid)
	next_link = get_next(aid)

	artFile = os.path.join("../article", art[3].split("/")[-1])
	f = open(artFile, "r")
	s = f.read()
	f.close()

	rePrev = re.compile(r"id='pervLink' href=\"([\s\S]*?)\"")
	s = rePrev.sub("id='pervLink' href=\"%s\"" % prev_link,s)
	reNext = re.compile(r"id='nextLink' href=\"([\s\S]*?)\"")
	s = reNext.sub("id='nextLink' href=\"%s\"" % next_link,s)

	f = open(artFile, "w")
	f.write(s)
	f.close()

	indexDtstr = processDatetime(str(art[1]))
	articles.append({
		#"datetime": indexDtstr['index'],
		"date": indexDtstr['indexD'],
		"time": indexDtstr['indexT'],
		"title": art[0],
		"brief": art[2],
		"permalink": art[3]
		})
tpl = Tpl(tfile="index.tpl")
output = tpl.render(articles = articles)

f = open("../index.html","w")
f.write(output)
f.close()

log("Done!")
		
"""
Var = {
#		articles = {
#			datetime: "yyyy-mm-dd hh:mm",#datetimeStr['index']
#			date: "dd Mmm yyyy",#datetimeStr['indexD']
#			time: "hh:mm",#datetimeStr['indexT']
#			title: "TITLE",
#			brief: "BRIEF"
#		}
#	}
"""
















