#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import sys


def set(comm):
    if len(comm) <> 3:
        raise TypeError('(error) Err')
#键不能为 “'”或者“"”,也就是说单引号和双引号不能为键
    try:
        d1 = {comm[1]:comm[2]}
    except NameError,msg:
        print '你的输入格式有误',msg

def get(comm):
    if len(comm) <> 2:
        raise TypeError

def auth(comm):
    if len(comm) <> 3:
        raise TypeError

def url(comm):
    if len(comm) <> 3:
        raise TypeError

def quit(comm):
    str = comm[0].lower()
    if str == 'quit': 
	raise KeyboardInterrupt

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
