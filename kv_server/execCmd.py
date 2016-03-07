#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import pickle
import os
try:
    import yaml

except ImportError:
    print '没有yaml库'
import requests
#def process(data):
#    
#
#    stream = open('data.yaml')
#    dict0 = yaml.load(stream)
##遗留问题：上一步会出现一个问题，就是如果data.yaml可能会是空，不是字典型，在server段要初始化一个字典
#
#    dict1 = yaml.load(data)
#    dict0.update(dict1)
#    stream = open('data.yaml','rb+')
#    yaml.dump(dict0,stream)
#    stream.close()
#    return "OK."
#lag = 0

#加载服务器端本地数据
def loadDict():
    file_1 = open('data.pickle','rb+')
    dict0 = pickle.load(file_1)
    file_1.close()
    return dict0

#更新服务器端数据
def updateDict(dict,tobe):
    file_2 = open('data.pickle','rb+')
    dict.update(tobe)
    pickle.dump(dict,file_2)
    file_2.flush()
    file_2.close()

#服务端更新模块
def set(array):
#array的格式是['key', 'val']
#    if Flag == 1:
#要提交的数据为 {'key':'val'}
        tobe = {array[0]:array[1]}
#从文件中加载原来数据
        dict1 = loadDict()
#更新原来数据
        updateDict(dict1,tobe)
        return 'OK'
#    else:
#        return '(error) Authentication required'

#get模块，用户获取对应key的val
def get(array):
#    if Flag == 1:
        key = array[0]
        dict2 = loadDict()
        return str(dict2.get(key,'None'))
#    else:
#        return '(error) Authentication required'

#用户认证模块
def auth(array):
    try:
        f = open('auth.conf','rb')
        authDict = yaml.load(f)
        f.close()
    except (NameError,IOError):
        return '(服务端错误)，auth.conf不存在,无法完成认证'

    if array[0] in authDict and array[1] == authDict[array[0]]:
        global Flag
        Flag = 1
        return '0'
    else:
        return '-1'

def url(array):
#    ['key','url']
    if Flag == 1:
	val = str(get(array))
	if val <> 'None':
#        st = array[0] + val
	    return array[0]+': '+ val
	else:
	    try:
		r = requests.get(array[1])
		status = r.status_code
#        size = len(r.content)
		size = r.headers['content-length']
		l1 = [status,size]
		listTobe = [array[0],l1]
		return set(listTobe)
	    except requests.exceptions.ConnectionError,msg:
		return str(msg)
	    except requests.exceptions.MissingSchema,msg:
		return str(msg)
	    except requests.exceptions.InvalidSchema,msg:
		return str(msg)
	    except requests.exceptions.InvalidURL,msg:
		return str(msg)
    else:
	return '(error) Authentication required '
        
#在每个连接线程启动时，初始化全局变量Flag为0，禁止用户在未授权情况下登陆
def setFlag():
    global Flag
    Flag = 0

#测试函数
def testflag(array):
    return str(Flag)
