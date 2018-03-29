__author__ = 'Pavel V. Bass'

import psycopg2
import sys, os

import json
import zlib


class Database(object):
    def __init__(self, db):
        self._db = db.copy()
        self._conn = None
        self._cur = None

    def connect(self):
        self.disconnect()
        self._conn = psycopg2.connect(**db)
        self._conn.autocommit = False
        self._cur = self._conn.cursor()

    def disconnect(self):
        if self._cur is not None:
            try:
                self._cur.close()
            except:
                pass
        if self._conn is not None:
            try:
                self._conn.close()
            except:
                pass
        self_conn, self._cur = None, None

    def get_max_sources_id(self):
        self._cur.execute('SELECT MAX(id) FROM sources;')
        return self._cur.fetchone()[0]

    def get_sources(self, heigh_id=None, limit=1000):
        if heigh_id is None:
            return tuple()

        q = 'SELECT id, domain_id, http, html, specific FROM sources WHERE ' \
            'id<%s AND  http_status=200 AND pudge_status=0 ' \
            'ORDER BY id LIMIT %s;'
        self._cur.execute(q, (heigh_id, limit))
        return self._cur.fetchall()

    def get_num_valid_sources(self):
        q = 'SELECT COUNT(*) FROM SOURCES WHERE http_status=200 AND pudge_status=0;'
        self._cur.execute(q)
        return self._cur.fetchone()[0]


def _status_bar(num_all):
    os.system('setterm -cursor off')
    bar_length = 100
    numbers_len = len(str(num_all))
    bar = '\r[%s] %3.2f%%    (%'+str(numbers_len)+'d/'+str(num_all)+')'
    yield
    n = 1
    print ''
    while True:
        proc = n*100.0/num_all
        _bar = '%-100s' % ('='*int(proc+0.5),)
        s = bar %(_bar, proc, n,)
        l = len(s)
        sys.stdout.write(s)
        sys.stdout.flush()
        mess = yield
        if mess is not None:
            break
        n += 1
    print ''
    os.system('setterm -cursor on')
    yield
    yield

def main(db):
    DB = Database(db)
    DB.connect()
    max_id = DB.get_max_sources_id()
    num_all = DB.get_num_valid_sources()
    limit = 1000
    print '%s resources will be calculated' % num_all
    num_calculated = 0
    sources = list()
    heigh_id = max_id + 1
    bar = _status_bar(num_all)
    bar.next()
    lens = dict()
    zip_len = 0
    while True:
        if not sources:
            sources = DB.get_sources(heigh_id, limit)
            if not sources:
                break
        s = sources.pop()
        if s[0] < heigh_id:
            heigh_id = s[0]
        html = s[3]
        zip_len += len(html)
        html = zlib.decompress(html)
        l = len(html)
        if s[1] not in lens:
            lens[s[1]] = list()

        lens[s[1]].append(l)
        bar.next()
    lens['zip_len'] = zip_len
    lens_json = json.dumps(lens)
    bar.send('')
    with open('lens.json', 'w') as f:
        f.write(lens_json)
    print '\nSaved into `lens.json` file.'
    for id in lens:
        if not isinstance(id, int):
            print id, ' - ', lens[id]
            continue
        print 'ID: %s' % id
        maximal = max(lens[id])
        minimal = min(lens[id])
        size = sum(lens[id])
        l = len(lens[id])
        print '   Max: %s bytes = %.3f KB, min: %s bytes = %.3f KB, average: %s bytes = %.3f KB' % \
              (maximal, maximal/1024.0, minimal, minimal/1024.0, size/float(l), size/1024.0/l)

if __name__ == '__main__':
    db = {
        'user': 'pavel',
        'host': 'localhost',
        'database': 'comm',
        'password': 'pavel'
    }

    main(db)