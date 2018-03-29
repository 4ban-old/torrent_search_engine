import os
import sys
from socket import *
from datetime import datetime

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


if __name__ == '__main__':
    #ret_code = daemonize_process()

    # open("daemonize_server.log", "w").write(' Ooops!\n')
    #log_file = open("daemonize_server.log", "a")
    #log_file.write("== Hi there: %s\n" % datetime.now().ctime())



    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 15001))
    s.listen(5)

    while True:
        client, addr = s.accept()
        # log_file.write('Client from addr %s\n' % addr)
        resp = ''
        while True:
            chunk = client.recv(8192)
            resp += chunk
            if '\r\n\r\n' in resp:
                break
        print resp
        if 'GET /garmonbozia BOB/1.0' in resp:
            break
        else:
            # log_file.write('==\n%s\n' % resp)
            pass
        answer = "HTTP/1.0 200 OK\r\nServer: nginx\r\n" \
                 "Content-type: text/html; charset=UTF-8\r\n" \
                 "Connection: close\r\n\r\n"
        answer += """<html>
                    <head>
                        <title>Hi</title>
                    </html>
                    <body>
                        <p>Hi there</p>
                    </body>
                    </html>"""
        client.send(answer)
        client.close()
    #log_file.write('== Bye: %s\n' % datetime.now())
    #log_file.close()
    #sys.exit(ret_code)
