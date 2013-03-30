#!/usr/bin/python
#-*- coding: utf8 -*-
import sys, re
import os.path
import yaml
from datetime import datetime
from jinja2 import Template
from genUtils import *
class Gen:
	BASE = '/'#http://sniky.github.com'
	LOG = True
	def __init__(self, blog = ''):
		self.proConf()

		self.v = self.env['version']
		self.blog = self.env['blogRoot']
		self.Tmpl = self.env['TemplateRoot']

		self.craft = open(blog)
		self.rawCraft = self.craft.read()
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
		tmpStream = self._loadRender(os.path.join(self.Tmpl, 'sub_info.html'), subInfo)

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
		tmpStream = self._loadRender(os.path.join(self.Tmpl, 'blog_body.html'), blogBody)

		#create blog page
		blogDir = os.path.join(self.blog, self.article.cate)
		blogFileName = self.article.permalink.split('/')[-1]

		self._log("Create blog page <%s>" %  os.path.join(blogDir, blogFileName))

		blogFile = open(os.path.join(blogDir, blogFileName), 'w')
		blogFile.write(tmpStream)
		blogFile.close()
	def _loadRender(self, tpl, var):
		try:
			tplFile = open(tpl)
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
	def __del__(self):
		self.craft.close()
def main():
	if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
		sys.exit("\nArgument Error\n")
	g = Gen(sys.argv[1])
	g.write()
if __name__ == '__main__':
	main()
