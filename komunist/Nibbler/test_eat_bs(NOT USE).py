# coding: utf-8
__author__ = 'Dmitry Kryukov'
from BeautifulSoup import BeautifulSoup
import re

html = '''<html>
                <head>
                <meta charset="windows-1251">
                <meta content="description of topic" name="description">
                <meta content="keywords for topic" name="keywords">

                <title>title for topic</title>

                <link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
                <link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

                </head>
            <body>
                <div class="post_body">
                    <span class="polor">
                        <a class="p-color">Some text inside first main div</a>
                        <a class="p-color">second a - p-color</a>
                    </span>

                    <a class="p-color">third a - p-color</a>
                    <p id="bold">
                        bold text
                        <ul>
                            <li class="list">one li</li>
                            <li>second li</li>
                        </ul>
                    </p>
                    text inside first div
                    <div>
                        text inside div
                    </div>
                    text inside first div
                </div>
                <div class="post_body">
                    <a>text inside second main div</a>
                </div>
                <div class="post_body">
                    <span>third div</span>
                </div>
                <div class="post_body">
                    <p>four div</p>
                </div>
                <div class="post">
                    div class postbody or class post
                </div
            </body>
        <html>'''

# ======================================================================
# settings (rutracker)
# ======================================================================
settings = dict()
settings['Nibbler'] = dict()
settings['Nibbler']['path_to_source'] = {'name': 'div',
                                         'class': 'post_body',
                                         'child': {'name': 'a', 'class': 'p-color', 'position':'2', 'or': {'name':'a','class':'p-color'}}
                                        }
settings['Nibbler']['path_to_source2'] = {'name': 'div',
                                         'id': 'post_body',
                                         'child': {'name': 'span', 'class': 'trew', 'position': '2'},
                                        }
settings['Nibbler']['path_to_source3'] = {'name': 'div',
                                         'class': 'postbody',
                                         'or': {'name': 'div', 'class': 'post'},
                                        }

settings['Nibbler']['path_to_category'] = {'name': 'td',
                                           'class': 'nav w100 pad_2',
                                           'child': {'name': 'a', 'position': '-1', 'target': 'text'}
                                           }
settings['Nibbler']['rules'] = {'b': [{'name': 'span', 'class': 'h1', 'id': 0}, {'name': 'p', 'id': 'bold'}],
                                'h1': [{'name': 'h1'}, {'name': 'a', 'class': 'p-color'}],
                                'h2': [{'name': 'h2'}, {'name': 'li', 'class': 'list'}],
                                'h3': [{'name': 'h3'}],
                                'h4': [{'name': 'h4'}],
                               }

# text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findNextSiblings(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})[int(settings['Nibbler']['path_to_source']['position'])-2]]
# text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]

# TODO: exceptions for each text =

def _source_parse(settings, soup):
    if 'path_to_source' in settings['Nibbler']:
        if 'child' in settings['Nibbler']['path_to_source']:
            if 'position' in settings['Nibbler']['path_to_source']['child']:
                if settings['Nibbler']['path_to_source']['child']['position'] < '2':
                    if 'or' in settings['Nibbler']['path_to_source']['child']:
                        try:
                            print '+++++++++++ child, position = 1, not or +++++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).find(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']})]
                            if not text:
                                raise
                        except:
                            print '+++++++++++ child, position = 1, or +++++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).find(settings['Nibbler']['path_to_source']['child']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['or']['class']})]
                    else:
                        print '+++++++++ child, position in child = 1, no or ++++++++++'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).find(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']})]
                else:
                    if 'or' in settings['Nibbler']['path_to_source']['child']:
                        try:
                            print '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findAll(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']}, limit=settings['Nibbler']['path_to_source']['child']['position'])[-1]]
                            if not text:
                                raise
                        except:
                            print '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findAll(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']}, limit=settings['Nibbler']['path_to_source']['child']['position'])[-1]]
                    else:
                        print '\nNOT WORK\n'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findAll(settings['Nibbler']['path_to_source']['child']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['or']['class']}, limit=settings['Nibbler']['path_to_source']['child']['position'])[-1]]
            else:
                if 'or' in settings['Nibbler']['path_to_source']['child']:
                    try:
                        print '+++++++++ child, no position, not or ++++++++++'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findAll(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']})]
                        if not text:
                            raise
                    except:
                        print '+++++++++ child, no position, or ++++++++++'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).findAll(settings['Nibbler']['path_to_source']['child']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['or']['class']})]
                else:
                    print '++++++++++++++ child, no position, no or +++++++++++'
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}).find(settings['Nibbler']['path_to_source']['child']['name'], attrs={'class': settings['Nibbler']['path_to_source']['child']['class']})]
        else:
            if 'position' in settings['Nibbler']['path_to_source']:
                if settings['Nibbler']['path_to_source']['position'] < '2':
                    if 'or' in settings['Nibbler']['path_to_source']:
                        try:
                            print '++++++++++ position = 1 not or in or +++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            print '++++++++++ position = 1 or in or +++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['or']['class']})]
                    else:
                        print '++++++++++++ position = 1 +++++++++++++'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]
                else:
                    if 'or' in settings['Nibbler']['path_to_source']:
                        try:
                            print '+++++++++++++ position > 1 and or in or ++++++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}, limit=int(settings['Nibbler']['path_to_source']['position']))[-1]]
                            if not text:
                                raise
                        except:
                            print '+++++++++++ position > 1 and not or in or ++++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['or']['class']}, limit=int(settings['Nibbler']['path_to_source']['or']['position']))[-1]]
                    else:
                        print '++++++++++++++ position > 1 +++++++++++++'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}, limit=int(settings['Nibbler']['path_to_source']['position']))[-1]]
            else:
                if 'or' in settings['Nibbler']['path_to_source']:
                    if 'position' in settings['Nibbler']['path_to_source']['or']:
                        if settings['Nibbler']['path_to_source']['or']['position'] < '2':
                            try:
                                print '+++++++++ position = 1 and not or in or ++++++++++++++'
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]
                                if not text:
                                    raise
                            except:
                                print '+++++++++ position = 1 and or in or ++++++++++++++'
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['Nibbler']['path_to_source']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['or']['class']})]
                        else:
                            try:
                                print '+++++++++ position > 1 and not or in or ++++++++++++++'
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']}, limit=int(settings['Nibbler']['path_to_source']['or']['position']))[-1]]
                                if not text:
                                    raise
                            except:
                                print '+++++++++ position > 1 and or in or ++++++++++++++'
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['or']['class']}, limit=int(settings['Nibbler']['path_to_source']['or']['position']))[-1]]
                    else:
                        try:
                            print '+++++++++++++ no such position in or and not or ++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            print '+++++++++++ no such position in or  and or ++++++++++++'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['or']['name'], attrs={'class': settings['Nibbler']['path_to_source']['or']['class']})]
                else:
                    print '++++++++++++++ no such position no or++++++++++++++'
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['Nibbler']['path_to_source']['name'], attrs={'class': settings['Nibbler']['path_to_source']['class']})]
    else:
        # can't chew it
        text = ''

    text = ''.join(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


soup = BeautifulSoup(html)
text = _source_parse(settings, soup)
print text