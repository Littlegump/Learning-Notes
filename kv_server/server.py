#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import socket
import sys
from thread import *
import os
import pickle
#try:
#    import urllib3
#except ImportError:
#    print '去安装urllib3库~'
#    sys.exit()
    

HOST,PORT = '',2076
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print '连接建立......'
    print '服务端已经启动!'
except socket.error, msg:
    print 'Bind Failed, Error code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

if not os.path.exists('data.pickle'):
    f = open('data.pickle','wb+')
    d = {}
    pickle.dump(d,f)
    f.flush()
    f.close()

module = __import__('execCmd')
def clntThread(conn):
    conn.sendall('welcome to the server\n')
    while True:
        data = conn.recv(1024)
        array = data.split()
#下面这个模块本来在这里，但是鉴于，后面的while 1 中也要用到，就讲module提出。       
#module = __import__('execCmd')
        func = getattr(module, array[0].lower())
        array.remove(array[0])
        reply = func(array)
        if not data:
            break
        conn.sendall(reply)
    conn.close()

while True:
    conn, addr = s.accept()
# 只要客户端重新初始化，就要调用setFlag函数将Flag重新置零,重新认证
    func = getattr(module,'setFlag')
    func()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clntThread,(conn,))

s.close()






