import os
import sys
from socket import *
from datetime import datetime
import time

UMASK = 0
WORKDIR = os.environ['HOME']
MAXFD = 1024
REDIRECT_TO = os.devnull


def daemonize_process():
    print "Ok, go"
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if pid == 0:
        os.setsid()
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        if pid == 0:
            os.chdir(WORKDIR)
            os.umask(UMASK)
        else:
            os._exit(0)
    else:
        os._exit(0)
    import resource
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD

    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

    return(0)


def simple_server(port, daemon=False, dir=''):
    if daemon:
        ret_code = daemonize_process()

    if not dir:
        dir = os.curdir
    dir = os.path.join(dir, 'server_pages')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)

    while True:
        client, addr = s.accept()
        # log_file.write('Client from addr %s\n' % addr)
        resp = ''
        _resp = ''
        while True:
            chunk = client.recv(8192)
            resp += chunk
            if _resp != resp:
                _resp = resp
                print '##### ',_resp

            if '\r\n\r\n' in resp:
                break
        r = resp.partition('\r\n')[0]
        r = r.split()
        path = r[1]
        if path and path[0] == '/':
            path = path[1:]
        if not path:
            path = 'index.html'
        file_path = os.path.join(dir, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            http_status = '200 OK'
            with open(file_path, 'rb') as f:
                answer = ''.join(f.readlines())
        else:
            http_status = '404 Not Found'
            answer = ''
            if os.path.exists(os.path.join(dir, '404.html')):
                with open(os.path.join(dir, '404.html')) as f:
                    answer = ''
                    for line in f:
                        answer += line
            else:
                answer = """<html><head><title>404</title></html>
                    <body><h1>Your princess is in another castle</h1>
                    </body></html>"""
        answer = '123456\n0123456789\nabcdefgh'
        if 'GET /garmonbozia BOB/1.0' in resp[:30]:
            break
        else:
            # log_file.write('==\n%s\n' % resp)
            pass
        answer_head = "HTTP/1.0 %s\r\nServer: nginx\r\n" \
                 "Content-type: text/html; charset=UTF-8\r\n" \
                 "Content-length: 1024\r\n" \
                 "Connection: close\r\n\r\n" % http_status
        # answer = answer_head + answer
        # answer = (str(x)[0]*16 for x in xrange(65535))
        client.send(answer_head)
        for a in answer:
            client.send(a)
            last = time.time()
            while True:
                now = time.time()
                if now - last > .2:
                    break

    
        client.close()
    if daemon:
        sys.exit(ret_code)

if __name__ == '__main__':
    simple_server(9000)
    # pass
    # open("daemonize_server.log", "w").write(' Ooops!\n')
    #log_file = open("daemonize_server.log", "a")
    #log_file.write("== Hi there: %s\n" % datetime.now().ctime())


    #log_file.write('== Bye: %s\n' % datetime.now())
    #log_file.close()
