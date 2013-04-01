#!/usr/bin/python
#-*- coding: utf8 -*-
import sys, re
import os.path
import yaml
from datetime import datetime
from jinja2 import Template
from genUtils import *
class Gen:
	CATE =  ['home', 'magic', 'psych', 'lifee']
	BASE = '/'#http://sniky.github.com'
	LOG = True
	def __init__(self, blog = '', action = None):
		self.proConf()

		self.v = self.env['version']
		self.blog = self.env['blogRoot']
		self.Tmpl = self.env['TemplateRoot']

		if action is None:
			self.craft = open(blog)
			self.rawCraft = self.craft.read()
		elif action == 'update':
			self.update()
	def update(self):
		#dump database article
		for cate in self.CATE:
			self.up = Updates(self.blog, self.Tmpl)
			allArticles = self.up.dump(cate)
			if len(allArticles) != 0:
				articleVars = []
				articleContainer = []
				for art in allArticles:
					tmpArt = Article(
							title = art[1],
							cate = art[3],
							author = 'me',
							permalink = art[4],
							dateline = datetime.strptime(str(art[2]), "%Y%m%d%H%M"))
					articleContainer.append(tmpArt)
					articleVars.append({
						'date': tmpArt.format_date()[:-6],
						'title': tmpArt.title,
						'permalink': tmpArt.permalink,
						})

				tmpStream = ''

				#load and render article list part
				self._log("Load and render article list part")
				tmpStream = self._loadRender('article_list_part.html', articleVars)

				#load and render home index page
				self._log("Load and render home index page")
				updateHome = {'now': cate, 'base': self.BASE, 'title': 'Sniky', 'articleList': tmpStream}
				tmpStream = self._loadRender('%s_index.html' % cate, updateHome)


				subDir = (cate == 'home') and '/' or '/'+cate
				indexFile = open(os.path.join(self.blog+subDir, 'index.html'),'w')
				indexFile.write(tmpStream)
				indexFile.close()

				for art in articleContainer:
					detailFilePath = os.path.join(self.blog, art.cate)
					detailFile = open(os.path.join(detailFilePath, art.permalink.split('/')[-1]))
					tmpStream = detailFile.read()
					detailFile.close()

					detailFile = open(os.path.join(detailFilePath, art.permalink.split('/')[-1]), 'w')

					rePrev = re.compile(r"id='pervLink' href='([\s\S]*?)'")
					rePrev.sub("id='pervLink' href='%s'" % art.get_prev(),tmpStream)

					reNext = re.compile(r"id='nextLink' href='([\s\S]*?)'")
					reNext.sub("id='nextLink' href='%s'" % art.get_next(),tmpStream)

					detailFile.write(tmpStream)
					detailFile.close()
	def write(self):
		self._parseBlogConfigArea()
		#manage article object
		self.article = Article(
				self.blogInfo['title'],
				self.blogInfo['cate'],
				self.blogInfo['author'],
				self.blogInfo['permalink'],
				datetime.today())
		self.tags = self.blogInfo['tags'].split(', ')
		if self.article.isnew():
			self._log("Article < %s > updated in datebase" % self.article.title)
			self.article.update()
		else:
			self.article.save()
			for tag in self.tags:
				self._log("Article add tag #%s#" % tag)
				self.article.tag(tag)
		tmpStream = ''

		#load and render subInfo
		self._log("Load and render subInfo")
		subInfo = {'date': self.article.format_date(), 'tags': self.tags, 'author': self.article.author}
		tmpStream = self._loadRender('sub_info.html', subInfo)

		#parse craft Markdown 
		self._log("Parse craft Markdown")
		tmpStream = Template(Md2HTML(self.rawBlogBody)).render(subInfo = tmpStream)

		#load and render blogBody
		self._log("Load and render blog body")
		blogBody = {
				'title': self.article.title,
				'base': self.BASE,
				'now': self.article.cate,
				'blogBody': tmpStream,
				'prev_link': self.article.get_prev(),
				'next_link': self.article.get_next()}
		tmpStream = self._loadRender('blog_body.html', blogBody)

		#create blog page
		blogDir = os.path.join(self.blog, self.article.cate)
		blogFileName = self.article.permalink.split('/')[-1]

		self._log("Create blog page <%s>" %  os.path.join(blogDir, blogFileName))

		blogFile = open(os.path.join(blogDir, blogFileName), 'w')
		blogFile.write(tmpStream)
		blogFile.close()
	def _loadRender(self, tpl, var):
		try:
			tplFile = open(os.path.join(self.Tmpl, tpl))
			tplStr = tplFile.read()
			tplFile.close()
		except:
			self._err('Failed to load and render template <%s>' % tpl)
		return Template(tplStr).render(Var = var)
	def _parseBlogConfigArea(self):
		reConf = r'(<conf[\s\S]*?>([\s\S]*?)<\/conf>)'
		res = re.match(reConf, self.rawCraft)
		self._log("Parsing Config area")
		if res is None:
			self._err('Confg area not found')
		res = re.findall(reConf, self.rawCraft)
		self.blogInfo = yaml.load(res[0][1])
		self.rawBlogBody = unicode(self.rawCraft[len(res[0][0]):], 'utf-8')
	def proConf(self):
		try:
			gconf = open('config.yaml').read()
			self.env = yaml.load(gconf)
		except:
			self._err('Failed to fetch config file <./config.yaml>')
	def _err(self, info):
		sys.exit('\n%s\n' % info)
	def _log(self, log):
		if self.LOG:
			print "\n%s\n" % log
def main():
	if len(sys.argv) == 2 and sys.argv[1] == 'update':
		g = Gen(action = 'update')
		sys.exit("\nUpdated\n")
	if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
		sys.exit("\nArgument Error\n")
	g = Gen(blog = sys.argv[1])
	g.write()

	flag = raw_input("Update Article Lists && Prev.Next relationship?[Y/N]")
	if flag in ['Y', 'y']:
		g.update()
	elif flag in ['N', 'n']:
		sys.exit("\nExit. Article lists and Article relationship are not updated\n")
if __name__ == '__main__':
	main()
