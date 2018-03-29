# coding: utf-8

__author__ = 'Dmitry Kryukov'

import psycopg2
import json
import collections
import zlib
import time

from komunist.Nibbler import version as nibbler_version
from komunist.tools import int_version
from komunist.tools.structures import AnyMethod


Domain = collections.namedtuple("DomainRecord", 'id domain specific', verbose=False)
Source = collections.namedtuple("SourceRecord", 'id domain_id http html specific', verbose=False)
Durl = collections.namedtuple("DurlRecord", "id pargs specific", verbose=False)
NotDisSource = collections.namedtuple("NotDismemberedSource",
                                      "id domain_id html specific", verbose=False)


class DataBaseMixin(object):
    def __init__(self, db, logger=None):
        """
        :param db: Dict of named arguments for
                   psycopg2.connect()
                   db= {database: '',
                        user: '',
                        password: '',
                        host: '',
                        port: ''
                        }
        :return: None
        """
        self._db = db.copy()
        self._conn = None
        self._cursor = None
        self._domains = None
        if logger is None:
            logger = AnyMethod()
        self._logger = logger

    def connect(self):
        self.disconnect()
        try:
            self._conn = psycopg2.connect(**self._db)
        except:
            # TODO what to do if can not connect? except logging
            self._logger.warning('I can\'t connect to database.')
            raise
        else:
            self._conn.autocommit = False
            self._cursor = self._conn.cursor()
            self._logger.info('Connection to database: database=%s, user=%s' % (self._db['database'], self._db['user']))

    def disconnect(self):
        if self._cursor is not None:
            try:
                self._cursor.close()
            except:
                pass
            self._cursor = None
            self._logger.info('Cursor closed.')
        if self._conn is not None:
            try:
                self._conn.close()
            except:
                pass
            self._conn = None
            self._logger.info('Connection closed.')


class NibblerDataBase(DataBaseMixin):

    def get_html(self, num=200, domain_id=None):
        """
            Function get htmls from sources table. Adding it into named tuple
                Source(id, domain_id, http, html, specific)
        :param num: limit for query
        :param domain_id: random trackers or one
        :return: htmls = namedtuples like Source(id domain_id http html specific)
        """
        if domain_id is None:
            q = 'SELECT id, domain_id, http, html, specific ' \
                'FROM sources WHERE http_status=200 AND pudge_status<2 AND not chewed LIMIT %s;'
            self._cursor.execute(q, (num,))
            self._logger.info('Request pack (%s) of html pages without domain_id (All trackers)' % num)
        else:
            q = 'SELECT id, domain_id, http, html, specific ' \
                'FROM sources WHERE domain_id=%s AND http_status=200 AND pudge_status<2 AND not chewed LIMIT %s;'
            self._cursor.execute(q, (domain_id, num))
            self._logger.info('Request pack (%s) of html pages with domain_id=%s' % (num, domain_id))
        try:
            htmls = self._cursor.fetchall()
        except psycopg2.Error as err:
            self._logger.error('I can\'t execute query: %s' % err.pgerror)
            raise
        else:
            htmls = map(lambda x: Source(x[0], x[1], zlib.decompress(x[2]), zlib.decompress(x[3]),
                                              json.loads(x[4].decode('string_escape'))), htmls)
            self._logger.debug('Send pack to nibbler.')
            return htmls

    def save_parsed(self, parsed_queue):
        """
            Save parsed pack into database.
        :param parsed_queue: Sequence of tuples (source, parsed, specific) where parsed is dictionary:
            {'url':'-',
            'title':'text',
            'meta_keywords':'text',
            'meta_description':'text',
            'category':'number',
            'text':[('t','text'),('b',' bold text')],}
        """
        # TODO: Read psycopg2 documentation about multi-insert
        '''
            Instead execute we can use executemany. For example:
                namedict = ({"first_name":"Joshua", "last_name":"Drake"},
                            {"first_name":"Steven", "last_name":"Foo"},
                            {"first_name":"David", "last_name":"Bar"})
            cursor.executemany("""INSERT INTO bar(first_name,last_name) VALUES (%(first_name)s, %(last_name)s)""", namedict)
        '''
        q = 'INSERT INTO chewed (domain_id, source_id, nibbler_status, page, version, specific) ' \
            'VALUES (%s, %s, %s, %s, %s, %s);'

        qq = 'UPDATE sources SET chewed=TRUE where id=%s;'
        _time_upload = time.time()
        while parsed_queue:
            source, parsed, specific = parsed_queue.pop()
            self._cursor.execute(q, (source.domain_id, source.id, specific['nibbler_status'],
                                     json.dumps(parsed), int_version(nibbler_version()), json.dumps(specific)))
            self._cursor.execute(qq, (source.id,))
        try:
            self._conn.commit()
            _time_upload = time.time() - _time_upload
            self._logger.info('Uploading pack of parsed texts into database is successful on `%3.2f` seconds.', _time_upload)
        except Exception as err:
            self._logger.error('I can\'t commit all executes. err=%s', err)
            # TODO save unsaved pack into file
            raise
        else:
            return _time_upload

    def get_domains(self, no_cache=False):
        """
        :return: Dictionary where:
                    key - domain_id
                    value - namedtuple Domain.
        """
        if no_cache or self._domains is None:
            q = 'SELECT id, domain, specific FROM domains;'
            try:
                self._cursor.execute(q)
            except psycopg2.Error as err:
                self._logger.error('I can\'t execute query: %s' % err.pgerror)
            else:
                self._domains = self._cursor.fetchall()
                try:
                    self._domains = {v[0]: Domain(v[0], v[1], json.loads(v[2].decode('string_escape')))for v in self._domains}
                except ValueError as err:
                    self._logger.error('Wrong data in table: %s' % err)
                    raise
        return self._domains


class ActuariusDataBase(DataBaseMixin):
    def __init__(self, db, logger=None):
        super(ActuariusDataBase, self).__init__(db, logger)
        self._durls_in_work = dict()

    def get_domains(self):
        """ Read and save in self all domains
            :return: None
        """
        q = 'SELECT id, domain, specific FROM domains' #' ORDER BY id ASC LIMIT 10;'
        self._cursor.execute(q)
        _domains = self._cursor.fetchall()
        self._conn.commit()
        domains = dict()
        for d in _domains:
            domains[d[1]] = Domain(d[0], d[1], json.loads(d[2]))
            self._durls_in_work[int(d[0])] = set()
        self._domains = domains

    @property
    def len_domains(self):
        """
        :return: number of domains
        """
        if self._domains is not None:
            return len(self._domains)

    @property
    def domains(self):
        """ Return Copy of domains dictionary.

            Where keys are domain name string as "www.example.com"
            And value is a named tuple with `id`, `domain`,
            and `specific` attributes
            `id` - id in database
            `domain` same as key (domain name string)
            `specific` is a dictionary, saved as json
        """
        return self._domains.copy()

    def get_chewed(self):
        pass

    def save_chewed(self):
        pass
