#!/usr/bin/python
#-*- coding: utf8 -*-

from genUtils import article
from genUtils import mdtrans
#from genUtils import updates

from datetime import datetime
import sys
import os.path
import re
import yaml
from jinja2 import Template

LOG = True
TPL_ROOT = './Tmplates/'
BASE = '/'#http://sniky.github.com'

def updatePages():
	pass
def proArticle(conf):
	dateline = datetime.today()
	art = article.Article(conf['title'], dateline, dateline, 0, conf['cate'], conf['author'], permalink = conf['permalink'], tags = conf['tags'].split(', '))
	return art
def main():
	if len(sys.argv) != 3:
		sys.exit('\nArguments Error\n')
	try:
		craftFilePath = sys.argv[1]

		craftFile = open(craftFilePath)
		raw_craft = craftFile.read()
	except:
		sys.exit('\nFile open Error\n')

	if LOG:
		print "Creating Blog from %s into %s\n" % (sys.argv[1], sys.argv[2])

	reConf = r'(<conf[\s\S]*?>([\s\S]*?)<\/conf>)'

	res = re.match(reConf, raw_craft)
	if LOG:
		print "Parsing Config area..."
	if res is None:
		sys.exit('\nConfg area not found\n')
	else:
		res = re.findall(reConf, raw_craft)
		conf = yaml.load(res[0][1])
		raw_blog = unicode(raw_craft[len(res[0][0]):], 'utf-8')
	

	if LOG:
		print "Create Article object..."
	arti = proArticle(conf)

	if LOG:
		print "Parsing MarkDown from raw file %s" % sys.argv[1]
	blogBody = mdtrans.md2html(raw_blog)

	if LOG:
		print "Insert sub info of this blog..."
	subInfoPath = os.path.join(TPL_ROOT, 'sub-info.html')
	subInfoFile = open(subInfoPath)
	raw_subInfo = subInfoFile.read()
	subInfoTpl = Template(raw_subInfo)
	subInfoStr = subInfoTpl.render(tags = arti.tags, author = arti.author, date = arti.format_date())
	subInfoFile.close()

	if LOG:
		print "Create Blog body..."
	blogBodyTpl = Template(blogBody)
	blogBodyStr = blogBodyTpl.render(subInfo = subInfoStr)

	if LOG:
		print "Rendering the blog page..."
	indexPath = os.path.join(TPL_ROOT, 'detail_index.html')
	indexFile = open(indexPath)
	raw_index = indexFile.read()
	indexTpl = Template(raw_index)

	indexStr = indexTpl.render(base = BASE, blog_body = blogBodyStr, title = arti.title, next_link = arti.get_next(), prev_link = arti.get_prev())


	blogRoot = sys.argv[2]
	subDir = arti.cate
	blogDir = os.path.join(blogRoot, subDir)
	if LOG:
		print "Create blog in %s..." % blogDir

	blogHTML = open(os.path.join(blogRoot+'/'+subDir, arti.permalink.split('/')[-1]), 'w')
	blogHTML.write(indexStr)
	blogHTML.close()

	if LOG:
		print "Update page info, including Article lists & Tag lists..."
	updatePages()
if __name__ == '__main__':
	main()
