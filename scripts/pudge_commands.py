import psycopg2
import collections
from shell import _parse_args
#import Pudge


class PudgeCommands(object):
    def __init__(self):
        self.prefix = '_pudge_'
        self.conn = psycopg2.connect(database='comm', host='localhost',
                    password='pavel', user='pavel')
        self.cur = self.conn.cursor()

    def get_command(self, command):
        return getattr(self, self.prefix+command, None)

    def get_all_commands(self):
        commands = list()
        for m in dir(self):
            name = m[len(self.prefix):]
            command = self.get_command(name)
            if command is not None:
                commands.append((name, command))
        return commands

    def _pudge_domains(self):
        Domain = collections.namedtuple('Domain', ('id', 'domain', 'specific'), verbose=False)
        self.cur.execute('select * from domains;')
        
        for domain in map(Domain._make, self.cur.fetchall()):
            print '| %4d | %30s | settings.. |' % (domain.id, domain.domain)
        
    def _pudge_domain(self, args=None):
        Domain = collections.namedtuple('Domain', ('id', 'domain', 'specific'), verbose=False)
        args = _parse_args(args)
        if not args.names:
            print 'No domain name'
            return
        if args.names[0].isdigit():
            q = 'select * from domains where id = %s;'
        else:
            q = 'select * from domains where domain = %s;'
        self.cur.execute(q, args.names[0])
        domain = Domain._make(self.cur.fetchone())
        print '      ID: %s' % domain.id
        print '  DOMAIN: %s' % domain.domain
        print 'SPECIFIC: %s' % domain.specific
        if args.args[0] == 's':
            pass


