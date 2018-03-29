from settings import settings
from tools import daemonize_process, init_logging


def version():
    """
        Komunist version
    """
    return '0.1'


def int_version(v=None):
    """
        Numeric representation of version
    :return: integer
    """
    if v is None:
        v = version()
    return '%03d%03d' % tuple(map(int, v.split('.')))

