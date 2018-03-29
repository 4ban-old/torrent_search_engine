# -*- coding: utf-8 -*-
"""
    Client connects to server and get http, html
    :param HOST: like 'rutracker.org'
    :param PORT: default 80
    :param PATH: like '/forum/viewtopic.php?t=1234'
    :return http: string
    :return html: string
"""
__author__ = 'Dmitry Kryukov'

from socket import *

def make_request(HOST, PORT, REQUEST):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST,PORT))
    s.send(REQUEST)
    answer = ''
    while True:
        chunk = s.recv(1024)
        answer += chunk
        #yield
        if not chunk:
            break
    s.close()
    answer = answer.split('\r\n\r\n')
    http = answer[0]
    html = answer[1]
    return http, html

if __name__ == '__main__':
    HOST = 'rutracker.org'
    PORT = 80
    PATH = '/forum/viewtopic.php?t=4685375'
    REQUEST = 'GET '+PATH+' HTTP/1.0\r\nHost: '+HOST+'\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0\r\n\r\n'
    make_request(HOST, PORT, REQUEST)
    http, html = make_request(HOST, PORT, REQUEST)
    print http
    print '###############################'
    print html