# coding: utf-8
__author__ = 'Dmitry Kryukov'

import lxml.html.soupparser
import lxml.html
import re
import chardet
import pprint
import time
from HTMLParser import HTMLParser


def version():
    return '0.1'

# If you want use test functions
# from BeautifulSoup import BeautifulSoup
# ================================================= Tests functions ====================================================
# TODO: source parse function: not for release.
# NOTE: Can use it if you want use beautiful soup instead lxml.
def _source_parse(settings, soup):
    if 'path_to_source' in settings:
        if 'child' in settings['path_to_source']:
            if 'position' in settings['path_to_source']['child']:
                if settings['path_to_source']['child']['position'] < '2':
                    if 'or' in settings['path_to_source']['child']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']})]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                else:
                    if 'or' in settings['path_to_source']['child']:
                        try:
                            # '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
                            if not text:
                                raise
                        except:
                            # '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
                    else:
                        # '\nNOT WORK\n'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
            else:
                if 'or' in settings['path_to_source']['child']:
                    try:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                        if not text:
                            raise
                    except:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']})]
                else:
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
        else:
            if 'position' in settings['path_to_source']:
                if settings['path_to_source']['position'] < '2':
                    if 'or' in settings['path_to_source']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                else:
                    if 'or' in settings['path_to_source']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['position']))[-1]]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['position']))[-1]]
            else:
                if 'or' in settings['path_to_source']:
                    if 'position' in settings['path_to_source']['or']:
                        if settings['path_to_source']['or']['position'] < '2':
                            try:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                                if not text:
                                    raise
                            except:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                        else:
                            try:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                                if not text:
                                    raise
                            except:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                    else:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                else:
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
    else:
        # can't chew it
        text = ''

    text = ''.join(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


# TODO: category parse: Need to change path_to_source to path_to_category.
# NOTE: Can use it if you want use beautiful soup instead lxml.
def _category_parse(settings, soup):
    """
        Function get part of text with tags depending on the settings
    """

    # TODO: Crutches. Need to refactor.
    try:
        meta_keywords = ''.join(soup.find('meta', attrs={'name': 'keywords'})['content']).strip()
    except:
        meta_keywords = ''
    try:
        meta_description = ''.join(soup.find('meta', attrs={'name': 'description'})['content']).strip()
    except:
        meta_description = ''
    try:
        title = ''.join(soup.find('title').contents).strip()
    except:
        title = ''

    if 'path_to_source' in settings:
        if 'child' in settings['path_to_source']:
            if 'position' in settings['path_to_source']['child']:
                if settings['path_to_source']['child']['position'] < '2':
                    if 'or' in settings['path_to_source']['child']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']})]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                else:
                    if 'or' in settings['path_to_source']['child']:
                        try:
                            # '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
                            if not text:
                                raise
                        except:
                            # '\n NOT WORK\n'
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
                    else:
                        # '\nNOT WORK\n'
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']}, limit=settings['path_to_source']['child']['position'])[-1]]
            else:
                if 'or' in settings['path_to_source']['child']:
                    try:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
                        if not text:
                            raise
                    except:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).findAll(settings['path_to_source']['child']['or']['name'], attrs={'class': settings['path_to_source']['child']['or']['class']})]
                else:
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}).find(settings['path_to_source']['child']['name'], attrs={'class': settings['path_to_source']['child']['class']})]
        else:
            if 'position' in settings['path_to_source']:
                if settings['path_to_source']['position'] < '2':
                    if 'or' in settings['path_to_source']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                else:
                    if 'or' in settings['path_to_source']:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['position']))[-1]]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                    else:
                        text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['position']))[-1]]
            else:
                if 'or' in settings['path_to_source']:
                    if 'position' in settings['path_to_source']['or']:
                        if settings['path_to_source']['or']['position'] < '2':
                            try:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                                if not text:
                                    raise
                            except:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.find(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                        else:
                            try:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                                if not text:
                                    raise
                            except:
                                text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']}, limit=int(settings['path_to_source']['or']['position']))[-1]]
                    else:
                        try:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
                            if not text:
                                raise
                        except:
                            text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['or']['name'], attrs={'class': settings['path_to_source']['or']['class']})]
                else:
                    text = [child.strip() if isinstance(child, str) else str(child) for child in soup.findAll(settings['path_to_source']['name'], attrs={'class': settings['path_to_source']['class']})]
    else:
        # can't chew it
        category = 0

    categories = {u'фильмы': 1,
                  u'сериалы': 2,
                  u'музыка': 3,
                  u'книги': 4,
                  u'игры': 5}
    category = ''.join(category.contents).lower().strip().split(' ')
    for cat in category:
        if cat in categories.keys():
            category = categories[cat]
            break
    return category, title, meta_keywords, meta_description
# ======================================================================================================================


def _get_encoding(source):
    """
        Function get encoding by chardet module.
        Returning best encoding by probability
    :param source: html page
    :return: encoding: string
    """
    html = source.html
    enc = chardet.detect(html)
    encoding = enc['encoding']
    return encoding


def _wait_for():
    """
        Coroutine that takes a pause for ms milliseconds
        and returns num of self calls

    :param ms: milliseconds
    :return:
    """

    # Initialization
    counter = 0
    while True:
        ms = yield counter
        if ms is None:
            ms = 0
        until = time.time() + ms/1000.0
        time.sleep(until)
        counter += 1


def get_tag():
    """
        Method in automat. Parse html tag to dict. For example:
            <div class="post" id="23"> -> {'name':'div', 'class':'post', 'id':'23'}
    """
    result = dict()
    name = ''
    key = ''
    _key = ''
    value = ''
    _value = ''
    quote = ''
    was_equal = False

    symbol = yield
    if symbol == '<' and not name:
        symbol = yield
    while symbol != '>':
        if 'name' not in result:
            if name:
                if symbol == ' ':
                    result['name'] = name.lower()
                else:
                    name += symbol
            else:
                if symbol == ' ':
                    pass
                else:
                    name = symbol
        else:
            if not key:
                if not _key:
                    if symbol == ' ':
                        pass
                    else:
                        _key = symbol
                else:
                    if symbol == ' ' or symbol == '=':
                        if symbol == '=': was_equal = True
                        key = _key
                    else:
                        _key += symbol
            else:
                if not _value:
                    if was_equal:
                        if symbol == ' ':
                            pass
                        else:
                            if symbol not in ['"', "'"]:
                                _value = (None,)
                            else:
                                quote = symbol
                                _value = ' '
                    else:
                        if symbol == ' ':
                            pass
                        elif symbol == '=':
                            was_equal = True
                        else:
                            _value = (None,)
                else:
                    if symbol != quote and not isinstance(_value, tuple):
                        _value += symbol
                    else:
                        value = _value[1:] if not isinstance(_value, tuple) else None
                        result[key.lower()] = value
                        _key = ''
                        key = ''
                        _value = ''
                        value = ''
                        quote = ''

        symbol = yield

    if 'name' not in result:
        result['name'] = name.lower()
    elif key:
        value = _value[1:] if not isinstance(_value, tuple) else None
        result[key.lower()] = value
    if result['name'].startswith('/'):
        result['name'] = result['name'][1:]
        result['close'] = True
    else:
        result['close'] = False
    yield result


def get_text():
    """
        Method in automat. Get text from html code.
    """
    text = ''
    symbol = ''
    while symbol != '<':
        text += symbol
        symbol = yield
    yield text


def _compare_tags(tag_from_rules, tag):
    """
        Function check compares for tags.
    :param tag_from_rules:
    :param tag:
    :return:
    """
    equal = True
    for key in tag_from_rules:
        if key == 0: continue
        if key not in tag:
            equal = False
            break
        if tag[key] != tag_from_rules[key]:
            equal = False
            break
    return equal


def _confirm_tag(tag, rule, strict=True):
    """
        Function check what tag need to ignore.
        Finding rule `i` in specific['rules'] and ignoring it.
    :param tag: current tag
    :param rule: rule from specific['rules']
    :param strict:
    :return: boolean
    """
    tag = dict(tag)
    del tag['close']
    if strict and len(tag) != len(rule):
        return False
    for key in rule:
        if key not in tag:
            return False
        val = [tag[key]] if strict else tag[key].split(' ')
        if rule[key] not in val:
            return False
        del tag[key]

    if strict and tag:
        return False
    return True

# NOTE: #####################################
def _spoiler_tag(tag, rule, strict=True):
    """
    :param tag: current tag
    :param rule: rule from specific['rules']
    :param strict:
    :return: boolean
    """
    tag = dict(tag)
    del tag['close']
    del tag['ignored']
    if strict and len(tag) != len(rule):
        return False
    for key in rule:
        if key not in tag:
            return False
        val = [tag[key]] if strict else tag[key].split(' ')
        if rule[key] not in val:
            return False
        del tag[key]

    if strict and tag:
        return False
    return True


def _get_category(category, specific):
    """
        Function get category from page.
        1 type: if category is number in link like ./forum/path?f=456
        2 type: if category is picture like /forum/cr/23.gif
        3 type: if category is text like 'Фильм'
    :param category: string
    :param specific: settings from database for domain
    :return: category: number [0...5]
    """
    # category like number in link
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


def _automat(text):
    # Initialization automat for parsed['text']
    method = get_tag()
    method.send(None)
    automat = ''
    # NOTE: Place where 2 tests not works.
    list_of_results = list()
    for symbol in text:
        result = method.send(symbol)
        if result is not None:
            if automat:
                method = get_tag()
                method.next()
                automat = False

            else:
                method = get_text()
                method.next()
                automat = True

            list_of_results.append(result)
    # Deleting empty
    list_of_results = filter(lambda x: x != ' ' and x, list_of_results)
    return list_of_results


def _text_processing(list_of_results, specific):
    tags = list()
    list_of_texts = list()
    texts = list()
    last_mark = ''
    last_text = ''
    script = False
    first = True
    list_tags_to_ignore = specific['rules'].get('i', list())
    ignore_flag = False
    # NOTE: ##############################
    list_tags_spoiler = specific['rules'].get('sp', list())
    spoiler_flag = False
    sp_text = ''
    sp_texts = list()
    for item in list_of_results:
        ###################### Ignoring script tags ###################
        ###################### Do not change it #######################
        item_name = item['name'] if isinstance(item, dict) else None
        if item_name is not None:
            if item_name == 'script' and not item['close']:
                script = True
                continue
            else:
                script = False
        else:
            if script:
                continue
            else:
                script = False
        ###############################################################
        if isinstance(item, dict):
            if item['close']:
                _item = {'name': '%s_' % item['name']}
                while tags and _item['name'] != item['name']:
                    poped = tags.pop()
                    if poped['ignored']:
                        ignore_flag = False
                    if poped['spoiler']:
                        spoiler_flag = False
                    if poped['name'] == item['name']:
                        break
            else:
                if filter(lambda x: _confirm_tag(item, x), list_tags_to_ignore):
                    ignore_flag = True
                    item['ignored'] = True
                else:
                    item['ignored'] = False
                if filter(lambda x: _spoiler_tag(item, x), list_tags_spoiler):
                    spoiler_flag = True
                    item['spoiler'] = True
                else:
                    item['spoiler'] = False
                tags.append(item)
        else:
            if tags:
                tag = tags[-1]
            else:
                tag = dict()
            mark = 't'
            for key, tags_list in specific['rules'].items():
                if filter(lambda x: _compare_tags(x, tag), tags_list):
                    mark = key
                    break
            # texts.append((mark, item.strip(),))
            if first:
                first = False
                last_mark = mark

            if spoiler_flag:
                sp_text += item.strip()+' '

            if not ignore_flag and not spoiler_flag:
                if last_mark == mark:
                    last_text += item.strip()+' '
                    last_mark = mark
                else:
                    if last_text:
                        texts.append((last_mark, last_text.strip(),))
                        last_text = ''
                    texts.append((mark, item.strip(),))
                    if sp_text:
                        sp_texts.append(('sp', sp_text.strip(),))
                        sp_text = ''

    if last_text:
        texts.append((last_mark, last_text.strip(),))
    if sp_text:
        sp_texts.append(('sp', sp_text.strip(),))
    # NOTE: ##############################
    list_of_texts.append(texts)
    list_of_texts.append(sp_texts)
    return list_of_texts


def _html_parse(specific, html):
    """
        HTML parse with beautifulsoup parser in lxml library.
    :param specific: dictionary. It looks like:
                    specific = {'xpath_to_source': '//html/body',
                                'xpath_to_category': '//div[@class="category"]/text()',
                                'rules': {'b': [{'name': 'b', 'class': 'bold'}, {'name': 'b'}],
                                          'h1': [{'name': 'h1'}, {'name': 'div', 'class': 'header1'}]
                                          }
                                }
    :param html: lxml.html object. What soupparser creating.
    :return strings: text, category, title, meta_keywords, meta_description
    """
    # xpath_to_source = specific['xpath_to_source'] if 'xpath_to_source' in specific else ''
    # xpath_to_category = specific['xpath_to_category'] if 'xpath_to_category' in specific else ''
    # xpath_to_torrent = specific['xpath_to_torrent'] if 'xpath_to_torrent' in specific else ''
    xpath_to_source = specific.get('xpath_to_source', '//no')
    xpath_to_category = specific.get('xpath_to_category', '//no')
    xpath_to_category_extra = specific.get('xpath_to_category_extra', '//no')
    xpath_to_torrent = specific.get('xpath_to_torrent', '//no')
    # Unuseful below. Used in previous version.
    # xpath_to_source += '/descendant-or-self::*[not(name()="script")]/text()'

    meta_keywords = ''.join(html.xpath('//meta[@name="keywords"]/@content')).strip() or ''
    meta_description = ''.join(html.xpath('//meta[@name="description"]/@content')).strip() or ''
    title = ''.join(html.xpath('//title/text()')).strip() or ''
    # Use xpath_to_category like main subject and use xpath_to_category_extra like secondary.
    # Need for torrentino.com for example
    category = ''.join(html.xpath(xpath_to_category)).strip() or ' '.join(html.xpath(xpath_to_category_extra)).strip() or 0
    torrent = html.xpath(xpath_to_torrent) or ''

    try:
        parser = HTMLParser()
        txt = ''
        for elem in html.xpath(xpath_to_source):
            txt = elem.text + ''.join(lxml.html.tostring(e, pretty_print=True) for e in elem)
            txt = parser.unescape(unicode(txt, 'utf-8'))
    except:
        # exception does not happen
        txt = ''

    txt = re.sub(r'\s+', ' ', txt)
    txt = txt.strip()
    if not txt and not torrent:
        nibbler_status = 3  # root with links. Not topic, not news.
    elif txt and not torrent:
        nibbler_status = 4  #  Not topic. News.
    elif not txt and torrent:
        nibbler_status = 5  # No block, but link on torrent file exists
    else:
        nibbler_status = 0

    return nibbler_status, txt, category, title, meta_keywords, meta_description


def _eat(html, specific, nibbler_logger):
    """
        Protected function, eat raw html and return dictionary parsed with
            category number, title, description, keywords, url and text.
    :param html: Decoded string (html)
    :param specific: Look documentation to html_parse()
    :return: dictionary. It looks like:
            parsed = {'url': '',
                      'title': 'unicode text',
                      'meta_keywords': 'unicode text',
                      'meta_description': 'unicode text',
                      'category': 'integer number',
                      'text': [('t', 'word1'),
                               ('b', 'word2'),
                               ('t', 'word3'),
                               ('t', 'word4'),
                               ('h1', 'word5'),
                               ('t', 'word6')
                               ]
                     }
            parsed['text'][*][1] also unicode.
    """
    # ##############
    #
    # ##############
    if nibbler_logger is None:
        import logging
        nibbler_logger = logging
    parsed = dict()
    # ================= for tests functions: _source_parse() and _category_parse() =================
    # try:
    #     soup = BeautifulSoup(html)
    # except Exception as err:
    #     logging.error('Can\'t create DOM.' % err)
    #     raise
    #
    # text = _source_parse(settings, soup)
    # category, title, meta_keywords, meta_description = _category_parse(settings, soup)
    # ==============================================================================================
    # ##########################################
    # Parsing html by lxml.beautifulsoup parser
    # ##########################################
    try:
        html = lxml.html.soupparser.fromstring(html)
    except Exception as err:
        nibbler_logger.error('Can\'t create DOM by beautifulsoup parser from lxml.')
        nibbler_logger.error('Exception: %s.' % err)
        nibbler_status = 2
        parsed = {'category': 0,
                  'url': '',
                  'meta_keywords': u'',
                  'meta_description': u'',
                  'title': u'',
                  'text': []}
        nibbler_logger.warning('I returned empty parsed and `nibbler status` set 2.')
        return nibbler_status, parsed
        # raise

    # ########################################
    # Get text from parsed html (lxml objects)
    # ########################################
    _time_html_parse = time.time()
    nibbler_status, text, category, title, meta_keywords, meta_description = _html_parse(specific, html)
    _time_html_parse = time.time() - _time_html_parse
    nibbler_logger.debug('Getting text, title, category, keywords and description from html on: `%3.4f` seconds.', _time_html_parse)

    # #########################
    # Get category
    # #########################
    if nibbler_status == 3 or nibbler_status == 4:  # if root with links or news topic, set category = 0
        category = 0
    else:
        category = _get_category(category, specific)

    # #########################
    # Creating dict of results
    # #########################
    parsed['url'] = ''
    parsed['title'] = unicode(title)
    parsed['meta_description'] = unicode(meta_description)
    parsed['meta_keywords'] = unicode(meta_keywords)
    parsed['category'] = category

    # ####################################################
    # Automat allocates tags(dict) and text(str) into list
    # ####################################################
    list_of_results = _automat(text)

    # ######################################################################
    # Processing text to view: [('t', 'text'),('b', 'bold text')]
    # Also deleting script tag and other garbage from specific['rules']['i']
    # ######################################################################
    texts = _text_processing(list_of_results, specific)

    parsed['text'] = texts

    # ###############
    # For tests
    # ###############
    #pprint.pprint(parsed['text'])
    return nibbler_status, parsed

