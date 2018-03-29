__author__ = 'Pavel V. Bass'

import unittest

from Pudge.parseurl import (parseurl, ParseUrl, unparseurl,
                            _follow, join)


class TestParseUrl(unittest.TestCase):
    def test_full_url(self):
        url = 'http://ya.ru/abc/def/ind.php?b=3&a=2#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/abc/def/ind.php', (('a', '2'), ('b', '3')), 'Hh_1')
        self.assertEqual(parseurl(url), res)
        
        # unparse
        url = 'http://ya.ru/abc/def/ind.php?a=2&b=3#Hh_1'
        self.assertEqual(unparseurl(res), url)
        
    def test_full_url_relatives(self):
        url = 'http://ya.ru/abc/../bcd/./def/ind.php?b=3&a=2#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/bcd/def/ind.php', (('a', '2'), ('b', '3')), 'Hh_1')
        self.assertEqual(parseurl(url), res)
        
        # unparse
        url = 'http://ya.ru/bcd/def/ind.php?a=2&b=3#Hh_1'
        self.assertEqual(unparseurl(res), url)

    def test_no_file_url(self):
        url = 'http://ya.ru/abc/def/?b=3&a=2#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/abc/def/', (('a', '2'), ('b', '3')), 'Hh_1')
        self.assertEqual(parseurl(url), res)

        # unparse
        url = 'http://ya.ru/abc/def/?a=2&b=3#Hh_1'
        self.assertEqual(unparseurl(res), url)

    def test_one_arg_url(self):
        url = 'http://ya.ru/abc/def/?a=2#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/abc/def/', (('a', '2'),), 'Hh_1')
        self.assertEqual(parseurl(url), res)
        
        # unparse
        self.assertEqual(unparseurl(res), url)

    def test_no_args_url(self):
        url = 'http://ya.ru/abc/def/#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/abc/def/', (), 'Hh_1')
        self.assertEqual(parseurl(url), res)

        # unparse
        self.assertEqual(unparseurl(res), url)


    def test_no_path_url(self):
        url = 'http://ya.ru/#Hh_1'
        res = ParseUrl(False, 'ya.ru', '/', (), 'Hh_1')
        self.assertEqual(parseurl(url), res)
        self.assertFalse(res.args)

        # unparse
        self.assertEqual(unparseurl(res), url)

        url_unparse = 'http://ya.ru/'
        url = 'http://ya.ru/'
        res = ParseUrl(False, 'ya.ru', '/', (), '')
        self.assertEqual(parseurl(url), res)

        # unparse
        self.assertEqual(unparseurl(res), url_unparse)

        url = 'http://ya.ru'
        res = ParseUrl(False, 'ya.ru', '/', (), '')
        self.assertEqual(parseurl(url), res)

        # unparse
        self.assertEqual(unparseurl(res), url_unparse)

    def test_no_http(self):
        url1 = '//ya.ru/abc/def/ind.php?b=3&a=2#Hh_1'
        url2 = 'ya.ru/abc/def/ind.php?b=3&a=2#Hh_1'
        url3 = 'ftp://ya.ru/abc/def/ind.php?b=3&a=2#Hh_1'
        res = ParseUrl(None, 'ya.ru', '/abc/def/ind.php', (('a', '2'), ('b', '3')), 'Hh_1')
        self.assertEqual(parseurl(url1), res)
        self.assertEqual(parseurl(url2), res)
        self.assertRaises(AttributeError, parseurl, url3)

    def test_no_domain(self):
        url = '/abc/def/i.php'
        res = ParseUrl(None, '', '/abc/def/i.php', (), '')
        self.assertEqual(res, parseurl(url))


class TestFollow(unittest.TestCase):
    def test_replace(self):
        path1 = '/a/'
        path2 = '/b/'
        self.assertEqual(path2, _follow(path1, path2))
        
    def test_add(self):
        self.assertEqual('/b', _follow('/', 'b'))
        self.assertEqual('/a/b', _follow('/a', 'b'))
        self.assertEqual('/a/b', _follow('/a/', 'b'))
        self.assertEqual('/a/b/', _follow('/a', 'b/'))

    def test_relative(self):
        self.assertEqual('/a/b/c', _follow('/a/b/d/', '../c'))
        self.assertEqual('/a/b/c/', _follow('/a/c/b', '../.././b/././c/d/../'))
        self.assertEqual('/a/b/c', _follow('/a/b/', '../b//c'))
        self.assertEqual('/a/b/c', _follow('f/../a/d/', '../b//c'))
        

class TestJoin(unittest.TestCase):
    def test_replace(self):
        base = 'http://example.com'
        url = '../a/b/c'
        self.assertEqual(parseurl('http://example.com/a/b/c'), join(base, url))

if __name__ == '__main__':
    unittest.main()
