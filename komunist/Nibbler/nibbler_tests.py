# coding: utf-8
"""
    Unittests for nibbler.
"""
__author__ = 'Dmitry Kryukov'

import unittest
import main
import logging
from komunist.tools import init_logging

init_logging('nibbler.log')
logger = logging.getLogger('TESTS')

class SimpleTests(unittest.TestCase):
    def test_simple(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>Фильмы онлайн</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                    </span>

                    <a class="p-color">1third a - p-color</a>
                    <p id="bold">
                        1bold text
                        <ul>
                            <li class="list">1one li</li>
                            <li>1second li</li>
                        </ul>
                    </p>
                    1text inside first div
                    <div>
                        1text inside div
                    </div>
                    text inside first div again
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        #result = ''
        result = (0, {'url': '',
                  'title': u'Фильмы онлайн',
                  'category': 0,
                  'meta_keywords': u'keywords for topic',
                  'meta_description': u'description of topic',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1third a - p-color'),
                           ('b', u'1bold text'),
                           ('t', u'1one li 1second li 1text inside first div 1text inside div'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_not_topic(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>Фильмы онлайн</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>


            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        #result = ''
        result = (3, {'url': '',
                  'title': u'Фильмы онлайн',
                  'category': 0,
                  'meta_keywords': u'keywords for topic',
                  'meta_description': u'description of topic',
                  'text': []
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_news_topic(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>Фильмы онлайн</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                    </span>

                    <a class="p-color">1third a - p-color</a>
                    <p id="bold">
                        1bold text
                        <ul>
                            <li class="list">1one li</li>
                            <li>1second li</li>
                        </ul>
                    </p>
                    1text inside first div
                    <div>
                        1text inside div
                    </div>
                    text inside first div again
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        #result = ''
        result = (4, {'url': '',
                  'title': u'Фильмы онлайн',
                  'category': 0,
                  'meta_keywords': u'keywords for topic',
                  'meta_description': u'description of topic',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1third a - p-color'),
                           ('b', u'1bold text'),
                           ('t', u'1one li 1second li 1text inside first div 1text inside div'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_comment_in_text(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>Фильмы онлайн</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                    </span>
                    <!-- comment -->
                    <a class="p-color">1third a - p-color</a>
                    <p id="bold">
                        1bold text
                        <ul>
                            <li class="list">1one li</li>
                            <li>1second li</li>
                        </ul>
                    </p>
                    1text inside first div
                    <div>
                        1text inside div
                    </div>
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div
                <td class="tCenter pad_6">
                    <p>
                        <a>вава</a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                     'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (0, {'url': '',
                  'title': u'Фильмы онлайн',
                  'category': 0,
                  'meta_keywords': u'keywords for topic',
                  'meta_description': u'description of topic',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1third a - p-color'),
                           ('b', u'1bold text'),
                           ('t', u'1one li 1second li 1text inside first div 1text inside div'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_nibbler_status_set_2(self):
        self.maxDiff = None
        html = 2

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (2, {'url': '',
                  'title': u'',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': []
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_nibbler_status_set_3(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">



                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_bo">
                </div>
                <div class="post_bod">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_b">
                    <span>3third div</span>
                </div>
                <div class="post">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (3, {'url': '',
                  'title': u'',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': []
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_nibbler_status_set_4(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">

                <title>Not finished</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <u>I will finish it later</u>
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (4, {'url': '',
                  'title': u'Not finished',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': [('t', u'I will finish it later')]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_text_before_last_tag(self):
        self.maxDiff = None
        html = '''<html>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                    </span>
                    <div>
                        1text inside div
                    </div>
                    ignored text
                </div>
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (0, {'url': '',
                  'title': u'',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1text inside div ignored text'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_text_without_tags(self):
        self.maxDiff = None
        html = '''<html>
            <body>
                <div class="post_body">
                    ignored text
                </div>
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (0, {'url': '',
                  'title': u'',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  #'text': []
                  'text': [('t', u'ignored text')]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_script_tag_without_other(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">

                <title>Not finished</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <script>
                        var a=10;
                        var b=20;
                        var c = a + b;
                        alert(c)
                    </script>
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div>
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (0, {'url': '',
                  'title': u'Not finished',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': []
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

    def test_script_tag_with_text(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">

                <title>Not finished</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                        <script>
                        var a=10;
                        var b=20;
                        var c = a + b;
                        alert(c)
                    </script>
                    </span>
                    <!-- comment -->
                    <a class="p-color">1third a - p-color
                                        <script>
                                            var a=10;
                                            var b=20;
                                            var c = a + b;
                                            alert(c)
                                        </script>
                    </a>
                    <p id="bold">
                        1bold text

                        <ul>

                            <li class="list">1one li</li>
                            <li>1second li</li>
                        </ul>
                    </p>

                    1text inside first div
                    <div>
                        1text inside div

                    </div>
                    <script>
                        var a=10;
                        var b=20;
                        var c = a + b;
                        alert(c)
                    </script>
                </div>
                <div class="post_body">
                    <div>
                    </div>

                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div>
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}]}}

        result = (0, {'url': '',
                  'title': u'Not finished',
                  'category': 0,
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1third a - p-color'),
                           ('b', u'1bold text'),
                           ('t', u'1one li 1second li 1text inside first div 1text inside div'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)

class TestsForDev(unittest.TestCase):
    def test_ignoring_garbage(self):
        self.maxDiff = None
        html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>Фильмы онлайн</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                    </span>

                    <a class="p-color">1third a - p-color</a>
                    <p id="bold">
                        1bold text
                        <ul>
                            <li class="list">1one li</li>
                            <li>1second li</li>
                        </ul>
                    </p>
                    1text inside first div
                    <div>
                        1text inside div
                    </div>
                    <div class="pad_2">
                        ignoring1
                        <div> ignoring2</div>
                        <span> ignoring3 <div>ignoring4</div></span>
                    </div>
                </div>
                <div class="post_body">
                    <a>2text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>3third div</span>
                </div>
                <div class="post_body">
                    <p>4four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div
                <td class="tCenter pad_6">
                    <p>
                        <a></a>
                    </p>
                </td>
            </body>
        <html>'''

        specific = {'xpath_to_source': '(//div[@class="post_body"])[1]',
                    'xpath_to_category': '//title/text()',
                    'xpath_to_torrent': '//td[@class="tCenter pad_6"]/p/a',
                    'rules': {'b': [{'name': 'p'}],
                              'i': [{'name': 'div', 'class': 'pad_2'}],
                              }
                    }

        #result = ''
        result = (0, {'url': '',
                  'title': u'Фильмы онлайн',
                  'category': 0,
                  'meta_keywords': u'keywords for topic',
                  'meta_description': u'description of topic',
                  'text': [('t', u'1Some text inside first main div 1second a - p-color 1third a - p-color'),
                           ('b', u'1bold text'),
                           ('t', u'1one li 1second li 1text inside first div 1text inside div'),
                           #('i', u'ignoring1 ignoring2 ignoring3 ignoring4'),
                           ]
                  })
        self.assertEqual(main.nibbler._eat(html, specific=specific, nibbler_logger=logger), result)


if __name__ == '__main__':
    unittest.main()
