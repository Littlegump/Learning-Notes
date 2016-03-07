#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import requests
import urllib3

def set(comm):
    if len(comm) <> 3:
        raise TypeError('(error) Err')
#键不能为 “'”或者“"”,也就是说单引号和双引号不能为键
    try:
        d1 = {comm[1]:comm[2]}
    except NameError,msg:
        print '你的输入格式有误',msg

#def quit(comm):
#    sys.exit()

def get(comm):
    if len(comm) <> 2:
        raise TypeError('(error) Err')

def auth(comm):
    if len(comm) <> 3:
        raise TypeError('(error) Err')

def url(comm):
    if len(comm) <> 3:
        raise TypeError('(error) Err')
#    try:
#	requests.get(comm[2])
#    except requests.exceptions.ConnectionError:
#        print 'ni de url youwenti'
#    except (requests.exceptions.MissingSchema,\
#		requests.exceptions.InvalidURL,\
#		urllib3.exceptions.LocationParseError):
#	raise requests.exceptions.MissingSchema(comm[2])

#test flag，测试函数
def testflag(comm):
    pass
