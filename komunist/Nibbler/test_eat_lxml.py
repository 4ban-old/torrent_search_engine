# coding: utf-8
__author__ = 'Dmitry Kryukov'
import re
import lxml.html.soupparser
import lxml.html


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
                        <a class="p-color">1Some text inside first main div</a>
                        <a class="p-color">1second a - p-color</a>
                        <p> this is text with: &copy; &reg; &lt; &gt;  special codes </p>
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
                    1text inside first div
                    <script>
                        var f = "hello"
                        alert("f")

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
                </div
            </body>
        <html>'''


# ======================================================================
# settings (rutracker)
# ======================================================================
specific = {'Nibbler': {'xpath_to_source': '(//div[@class="post_body"])[1]', # /*[not(name()="script")])
                        'xpath_to_category': '//td[@class="nav w100 pad_2"]/a[last()]/text()'
                        }
            }

specific['Nibbler']['rules'] = {'b': [{'name': 'span', 'class': 'h1', 'id': 0}, {'name': 'p', 'id': 'bold'}],
                                'h1': [{'name': 'h1'}, {'name': 'a', 'class': 'p-color'}],
                                'h2': [{'name': 'h2'}, {'name': 'li', 'class': 'list'}],
                                'h3': [{'name': 'h3'}],
                                'h4': [{'name': 'h4'}],
                               }


def html_parse(specific, html):
    xpath_to_source = specific['Nibbler']['xpath_to_source']
    xpath_to_category = specific['Nibbler']['xpath_to_category']
    #xpath_to_source += '/descendant-or-self::*[not(name()="script")]'
    try:
        meta_keywords = ''.join(html.xpath('//meta[@name="keywords"]/@content')).strip()
    except:
        meta_keywords = ''
    try:
        meta_description = ''.join(html.xpath('//meta[@name="description"]/@content')).strip()
    except:
        meta_description = ''
    try:
        title = ''.join(html.xpath('//title/text()')).strip()
    except:
        title = ''
    try:
        category = u' '.join(html.xpath('//title/text()'))
        if not category:
            raise
    except:
        category = 0
    categories = {u'фильмы': 1,
                  u'фильм': 1,
                  u'сериалы': 2,
                  u'сериал': 2,
                  u'книги': 3,
                  u'музыка': 4,
                  u'игры': 5}
    # ========================================================
    # text = html.xpath(xpath_to_source)
    # text = ' '.join(text)
    # c = requests.get('http://rutracker.org/forum/index.php').content
    #
    # tree = html.parse(StringIO(s))
    #
    # for elem in tree.xpath("//div[@class='category']"):
    #      print html.tostring(elem, pretty_print=True)

    #
    # for elem in html.xpath(xpath_to_source):
    #     print lxml.html.tostring(elem, pretty_print=True)
    # import lxml.html
    # text = html.xpath(xpath_to_source)
    # text = ''.join(text).strip()
    # print lxml.html.tostring(text)
    from HTMLParser import HTMLParser
    parser = HTMLParser()
    for elem in html.xpath(xpath_to_source):
        text = elem.text + ''.join(lxml.html.tostring(e, pretty_print=True) for e in elem)
        #text = parser.unescape(unicode(text, 'utf-8'))
    if isinstance(category, int):
        pass
    else:
        # TODO: ошибка AttributeError: 'str' object has no attribute 'contents'
        category = category.encode('utf-8')
        category = ''.join(category).lower().strip().split(' ')
        for cat in category:
            if cat in categories.keys():
                category = categories[cat]
                break
            else:
                category = 0
    print category
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    dd = dict()
    dd['url'] = None
    dd['title'] = title
    dd['meta_keywords'] = meta_keywords
    dd['meta_description'] = meta_description
    dd['text'] = text
    dd['category'] = category
    return dd


try:
    html1 = lxml.html.soupparser.fromstring(html)
except:
    raise

dd = html_parse(specific, html1)
for items in dd.items():
    print items
