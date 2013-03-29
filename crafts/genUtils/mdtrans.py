#!/usr/bin/python
#-*- coding: utf8 -*-

#set file unicode
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import misaka

def md2html(blog):
	return misaka.html(blog)
