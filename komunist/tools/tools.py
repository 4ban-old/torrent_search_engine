import os
import logging


def daemonize_process(pid_file=None):
    """ Make current process an unix daemon process

        Be aware that all current descriptors will be lost,
        so opening files, logging etc must be after this
        fumction. Current directory become a %HOME% directory
        of user that run this process.

        Original idea: http://code.activestate.com/recipes/278731/

        :param pid_file: path to pid file. If path was passed, function
            will check this path and will raise exception if such
            file exists. Because that can mean  this kind of Daemon
            is already run. If path was not passed (None) function
            will make daemon without checking a file.
    """

    UMASK = 0
    WORKDIR = os.environ['HOME']
    MAXFD = 1024
    REDIRECT_TO = os.devnull
    PID_FILE = os.path.join(WORKDIR, pid_file) if pid_file is not None else None

    if PID_FILE is not None and os.path.exists(PID_FILE):
        raise Exception("Possibly Daemon is already run. Remove pid file or stop Daemon first.")
    elif PID_FILE is not None:
        params = "process ID = %s\n" \
                 "parent process ID = %s\n" \
                 "process group ID = %s\n" \
                 "session ID = %s\n" \
                 "user ID = %s\n" \
                 "effective user ID = %s\n" \
                 "real group ID = %s\n" \
                 "effective group ID = %s\n" % \
                 (os.getpid(), os.getppid(),
                  os.getpgrp(), os.getsid(0),
                  os.getuid(), os.geteuid(),
                  os.getgid(), os.getegid()
                  )
        p = open(PID_FILE, "w")
        p.write(params)
        p.close()
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

def init_logging(log_file, level=None):
    """ Project settings for logs
    :param log_file: path to log_file
    :param level: level of logging
    """
    levels = {
        None: logging.INFO,
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARN,
        'CRITICAL': logging.CRITICAL
    }
    if level not in levels:
        level = None
    level = levels[level]

    logging.basicConfig(level=level,
                        format='%(asctime)s [%(process)s] %(name)-12s %(levelname)s %(message)s',
                        datefmt='%d.%m.%Y[%H:%M:%S]',
                        filename=log_file,
                        filemode='a')

domain_specific = {
    'specific_version': int(),
    'robots_txt': 1,
    'pudge': {
        'mirrors': list(),
        'last_ip': str(),
    },
    'nibbler': {
        'xpath_to_source': str(),
        'xpath_to_category': str()
    },
}