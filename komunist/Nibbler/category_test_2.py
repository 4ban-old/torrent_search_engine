# coding: utf-8
__author__ = 'Dmitry Kryukov'

from komunist.Nibbler.nibbler import _eat
import lxml.html.soupparser
import lxml.html

"""
0 - default
1 - audio
2 - book
3 - game
4 - video
5 - program
"""
specific_rutracker = {u'category': {u'4': [505],
                                    u'0': [23],
                                    u'3': [503],
                                    u'2': [43],
                                    u'5': [445],
                                    u'1': [556,565,54,43,4455,4532]},
                      u'xpath_to_category': u'//span[@class="brand-bg-white"]/a[last()]/@href',
                      }
specific_nnm = {u'category': {u'4': [885],
                              u'0': [23],
                              u'3': [88],
                              u'2': [43],
                              u'5': [445],
                              u'1': [556,565,54,43,4455,4532]},
                u'xpath_to_category': u'//span[@class="nav"]/a[last()]/@href',
                }
specific_tapochek = {u'category': {u'4': [40],
                                   u'0': [23],
                                   u'3': [18],
                                   u'2': [430],
                                   u'5': [43],
                                   u'1': [556,565,54,43,4455,4532]},
                     u'xpath_to_category': u'//td[@class="nav w100"]/a[last()]/@href',
                     }
specific_torrentino = {u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                                     u'0': [u''],
                                     u'3': [u'игры', u'игра', u'игрой', u'игр'],
                                     u'2': [u''],
                                     u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                                     u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
                       u'xpath_to_category': u'//div[@class="tagname"]/text()',
                       u'xpath_to_category_extra': u'//div[@class="tags"]/a/text()',
                       }
specific_tfile = {u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                                u'0': [u''],
                                u'3': [u'игры', u'игра', u'игрой', u'игр'],
                                u'2': [u''],
                                u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                                u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
                  u'xpath_to_category': u'//span[@class="path"]/descendant::*[last()]/text()',
                  }
specific_fasttorrent = {u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                                      u'0': [u''],
                                      u'3': [u'игры', u'игра', u'игрой', u'игр'],
                                      u'2': [u''],
                                      u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                                      u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
                        u'xpath_to_category': u'//div[@class="margin"]/a/text()',
                        }


html = """
<html>
    <body>
        +rutracker <span class="brand-bg-white">
                    <a href="./index.php">Список форумов rutracker.org</a>
                    <a href="./viewforum.php?f=7">Зарубежное кино</a>
                    <a href="./viewforum.php?f=505">Индийское кино</a>
                  </span>
        +nnm-club <span class="nav">
                    <a class="nav" href="index.php">Торрент-трекер NNM-Club</a>
                    <a class="nav" href="viewforum.php?f=318">Классика кино и Фильмы до 90-х</a>
                    <a class="nav" href="viewforum.php?f=885">Зарубежная Классика (HD)</a>
                 </span>
        +tapochek <td class="nav w100" style="padding-left: 8px;">
                    <a href="./index.php">Список форумов Tapochek.net</a>
                    <a href="index.php?c=5">Кинематограф</a>
                    <a href="viewforum.php?f=429">Новинки кинематографа</a>
                    <a href="viewforum.php?f=430">Новинки 2014-2015 (Rips)</a>
                 </td>
        +tfile <span class="path">
                <a href="/forum/">Каталог торрентов</a>
                <a href="/forum/?c=9">Софт</a>
                <a href="/forum/viewforum.php?f=1249">Linux, Unix и другие</a>
                 » Программы
              </span>
        +torrentino <div class="tagname">фильМы</div>
                   <div class="tags">
                        <a href="http://www.torrentino.com/search/12">игры</a>
                        <a href="http://www.torrentino.com/search/7764">Сталкер</a>
                    </div>
        +fast-torrent <div class="margin">
                        <a href="/most-films/">Фильмы</a>
                        / Из машины / Deus Ex Machina
                     </div>
        +kinozal <img class="cat_img_r" alt="" onclick="cat(45);" src="http://st.kinozal.tv/pic/cat/45.gif">

        megashara <table class="info-table">
                    <tbody>
                        <tr class="first">
                        <tr class="dark">
                            <td class="cell1">Год выхода:</td>
                            <td><a href="/movies?year=2014">2014</a></td>
                        </tr>
                        <tr class="">
                            <td class="cell1">Жанр:</td>
                            <td><a href="/movies/genre/16">Ужасы</a></td>
                        </tr>
                        <tr class="dark">
                        <tr class="">
                            <td class="cell1">Режиссер:</td>
                            <td><a href="/search/?text=%D0%94%D0%B6%D0%BE%20%D0%94%D0%B0%D0%BD%D1%82%D0%B5&where=director&all_words=0">Джо Данте</a></td>
                        </tr>
                        <tr class="dark">
                            <td class="cell1">В ролях:</td>
                            <td>
                                <a href="/search/?text=%D0%90%D0%BD%D1%82%D0%BE%D0%BD%20%D0%95%D0%BB%D1%8C%D1%87%D0%B8%D0%BD&where=cast&all_words=0">Антон Ельчин</a>
                                <a href="/search/?text=%D0%AD%D1%88%D0%BB%D0%B8%20%D0%93%D1%80%D0%B8%D0%BD&where=cast&all_words=0">Эшли Грин</a>
                                <a href="/search/?text=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80%D0%B0%20%D0%94%D0%B0%D0%B4%D0%B4%D0%B0%D1%80%D0%B8%D0%BE&where=cast&all_words=0">Александра Даддарио</a>
                                <a href="/search/?text=%D0%9E%D0%BB%D0%B8%D0%B2%D0%B5%D1%80%20%D0%9A%D1%83%D0%BF%D0%B5%D1%80&where=cast&all_words=0">Оливер Купер</a>
                                <a href="/search/?text=%D0%9E%D0%B7%D0%B8%D0%BE%D0%BC%D0%B0%20%D0%90%D0%BA%D0%B0%D0%B3%D0%B0&where=cast&all_words=0">Озиома Акага</a>
                                <a href="/search/?text=%D0%9C%D0%B0%D1%80%D0%BA%20%D0%90%D0%BB%D0%B0%D0%BD%20%D0%91%D1%80%D0%B0%D1%83%D0%BD&where=cast&all_words=0">Марк Алан Браун</a>
                                <a href="/search/?text=%D0%AD%D1%80%D0%B8%D0%BA%D0%B0%20%D0%91%D0%BE%D1%83%D0%B8&where=cast&all_words=0">Эрика Боуи</a>
                                <a href="/search/?text=%D0%93%D1%8D%D0%B1%D1%80%D0%B8%D1%8D%D0%BB%D0%BB%D1%8C%20%D0%9A%D1%80%D0%B8%D1%81%D1%82%D0%B8%D0%B0%D0%BD&where=cast&all_words=0">Гэбриэлль Кристиан</a>
                                <a href="/search/?text=%D0%90%D1%80%D1%87%D0%B8%20%D0%A5%D0%B0%D0%BD&where=cast&all_words=0">Арчи Хан</a>
                                <a href="/search/?text=%D0%A2%D0%BE%D0%BC%D0%BE%D0%BA%D0%BE%20%D0%9A%D0%B0%D1%80%D0%B8%D0%BD%D0%B0&where=cast&all_words=0">Томоко Карина</a>
                            </td>
                        </tr>
                    </tbody>
                 </table>
        lostfilm
        torrentinonet
        hdreactor
        sharlet
        uniongang
        soundpark
        bit2bit
        unionpeer
        torzona
        newserial
        torzone
        rusmedia



    </body>
</html>
"""

specific_ = {u'category': {u'4': [],
                                  u'0': [],
                                  u'3': [],
                                  u'2': [],
                                  u'5': [],
                                  u'1': []},
                    u'xpath_to_category': u'',
                    }

# #############################################
# #############################################
specific = specific_fasttorrent
def _html_parse(specific, html):
    xpath_to_category = specific.get('xpath_to_category', '//no')
    xpath_to_category_extra = specific.get('xpath_to_category_extra', '//no')
    category = ''.join(html.xpath(xpath_to_category)).strip() or ' '.join(html.xpath(xpath_to_category_extra)).strip() or 0
    return category


def _get_category(category, specific):
    # phpbb engine
    if '?f=' in category:
        try:
            category = category.split('=')[-1]
            category = int(category)
            old_category = category
            for key in specific['category']:
                if category in specific['category'][key]:
                    category = key
            if category == old_category:
                category = 0
        except:
            category = 0
    # category like picture
    elif filter(lambda x: x in category, ['.gif', '.png', '.jpg', '.jpeg', '.bmp', '.ico']):
        try:
            category = category.split('/')[-1]
            category = category.split('.')[0]
            category = int(category)
            old_category = category
            for key in specific['category']:
                if category in specific['category'][key]:
                    category = key
            if category == old_category:
                category = 0
        except:
            category = 0
    # category like text
    else:
        try:
            import re
            category = category.lower().strip()
            category = re.sub(ur"^\s+|,|\.|\s+$", '', category)
            category = category.split(' ')
            old_category = category
            for key in specific['category']:
                for cat in category:
                    if cat in specific['category'][key]:
                        category = key
            if category == old_category:
                category = 0
        except:
            category = 0
    return category

try:
    html = lxml.html.soupparser.fromstring(html)
except Exception as err:
    parsed = {'category': 0,
              'url': '',
              'meta_keywords': u'',
              'meta_description': u'',
              'title': u'',
              'text': []}

category = _html_parse(specific, html)

category = _get_category(category, specific)
parsed = dict()
parsed['category'] = category
print parsed['category']