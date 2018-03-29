# -*- coding: utf-8 -*-
"""
    Программа pudge, вытаскивает контент
    Зависимости: requests, lxml, psycopg2.
"""
__author__ = 'Dmitry Kryukov'

import lxml.html
import requests
import csv
import re
import psycopg2
import datetime
import json
import argparse
import ConfigParser

def create_parser():
    """
        Создает парсер аргументов.
        Перечисляем ожидаемые аргументы.
    """

    parser = argparse.ArgumentParser(description = 'Dofus is part of backend programm.')
    parser.add_argument('-u', '--url', help='Enter URL like: http://example.com/')
    parser.add_argument('-d', '--database', action='count', help='Get URL from database')
    return parser

def get_config():
    """
        Читает конфиг файл с настройками.
        По умолчанию лежит в корне проекта и имеет
        название pudge.cfg.
    """

    config = ConfigParser.ConfigParser()
    config.read('pudge.cfg')
    default_url = config.get('default','url')
    database = config.get('database','database')
    user = config.get('database','user')
    password = config.get('database','password')
    host = config.get('database','host')
    port = config.get('database','port')
    return default_url, database, user, password, host, port

def get_domain_from_database(database,user,password,host,port):
    """
        Получаем домены из базы данных.
        Таблица domains.
    """
    
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    print 'pudge: Соединение с базой данных установлено.'
    cur = conn.cursor()
    cur.execute("SELECT domain from domains")
    rows = cur.fetchall()
    domains = []
    for row in rows:
         domains.append(row[0])
    conn.commit()
    print 'pudge: Домен получен.'
    conn.close()
    return domains

def make_request(url):
    """
        Делает запрос на сервер.
        При зпросе имитируем браузер передавая user-agent
        Получает http ответ сервера и html код страницы. 
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}    
    resp = requests.get(url, headers=headers)
    resp.encoding = get_charset(resp.headers, resp.text) or 'utf-8'
    return dict(resp.headers), resp.text

def get_charset(http, html):
    """
        Поиск указаний кодировки в HTTP заголовках
        и в мета-тегах html страницы. 
        Если кодировка не найдена или 
        ответ содержит несколько слов 
        возвращается пустая строка.
    """

    cod = ''
    if 'charset' in http['Content-type']:
        if 'charset=' in http['Content-type']:
            cod = http['Content-type'].split('charset=')[-1]
        elif 'charset =' in http['Content-type']:
            cod = http['Content-type'].split('charset =')[-1]
        cod = cod.lstrip()
        s = ['\"','\'']
        if cod[0] in s:
            cod = cod[1:].partition(cod[0])[0]
        cod = cod.strip()
        cod = cod.lower()
        if ';' in cod:
            cod = cod.partition(';')[0]
            cod = cod.strip()
    else:
        meta = re.findall(r'<head([\s\S]*)</head>', html)
        if meta:
            charset = re.findall(r'<meta[^>]*charset=([^>]*)',meta[0])
            cod = ''.join(charset)
            if len(cod) > 3:
                cod = cod.lstrip()
                s = ['\"','\'']
                if cod[0] in s:
                    cod = cod[1:].partition(cod[0])[0]
                else:
                    cod = cod[0:].partition(s[0])[0]
                cod = cod.strip()
                cod = cod.lower()
            else:
                err = 'No coding in <meta>'
                print err
        else:
            err = 'Page has no <head>'
            print err
    return cod

def get_source(html,url):
    """
        Поиск ссылок на странице.
        source = ссылки на файлы, картинки, стили 
                и прочие внешние файлы
    """

    document = lxml.html.document_fromstring(html)
    source = set()
    source |= set(document.xpath('//link/@href'))
    source |= set(document.xpath('//script/@src'))
    source |= set(document.xpath('//img/@src'))
    # =================================
    """
    all_links = re.findall(r'http?://[^"^\']{3,}', html)
    extensions = ['ico','jpg','jpeg','png','bmp']
    for i in range(len(all_links)):
        print all_links[i][-4:]
        if all_links[i][-4:] in extensions:

    #(r'[/]{0,1}([^/]{1,}/){1,}[^"^\']',dop)
    """
    # =================================
    return list(source)

def get_durls(html, url):
    """
        Поиск ссылок на странице
        durls = ссылки навигации и тд.
    """

    document = lxml.html.document_fromstring(html)
    durls = document.xpath('//a/@href')
    durls = filter(lambda x: x != '',durls)
    return durls

def get_domain_durls(durls, url):
    """
        Выделяет из ссылки, корень, путь, аргументы.
        Логика поведения при разных типах ссылок.
        Возвращает список кортежей [(path,arg),(path,arg)]
    """

    durls = set(durls)
    url = url.replace('http://', '')
    domain = url.partition('/')[0]
    path = url.partition('/')[2]
    path = path.rpartition('/')[0]
    path = path.split('/')
    domain_durls = []
    for durl in durls:
        durl = durl.lower()
        durl = durl.strip()
        if  'http://' in durl:
            _durl = durl[7:]
            if '/' not in _durl:
                durl += '/'
                
        if '/' in durl:
            durl_args = durl.rpartition('/')[-1]
            durl = durl.rpartition('/')[0]
        else:
            durl_args = durl
            durl = ''
        if 'http://' in durl:
            durl = durl.replace('http://', '')

            durl_domain = durl.partition('/')[0]
            durl_path = durl.partition('/')[2]
        elif durl and durl[0] == '.':
            durl_domain = domain
            durl = durl.split('/')
            durl_path = path[:]
            for act in durl:
                if act == '.':
                    pass
                elif act == '..':
                    if durl_path:
                        durl_path.pop()
                else:
                    durl_path.append(act)
            durl_path = '/'.join(durl_path)
        elif durl and durl[0] == '/':
            durl_domain = domain
            durl_path = durl[1:]
        else:
            durl_domain = domain
            durl_path = '/'.join(path)+durl
        durl_path = '/%s/' % durl_path if durl_path else '/'
        if domain == durl_domain:
            domain_durls.append((durl_path, durl_args))
    return domain_durls

def save_to_csv(http, html, durls, source, name='output.csv'):
    """
        Функция сохранения данных в файл.
        По умолчанию файл называется output.csv
    """

    with open(name, 'w') as output: # Заменить w на a чтобы файл не затирался
        writer = csv.writer(output, delimiter='\t', quotechar='\n', quoting=csv.QUOTE_ALL)
        html = html.encode('utf-8') # Чтобы работало в python2.7.8
        writer.writerow([http, html, source, durls])

def write_to_db(url,http, html, source, durls_processed, database, user, password, host, port):
    """
        Запись данных в базу данных:
            pathes = domain, path.
            durls = path_id,args.
            content = durl_id,http,html,sources,datetime
    """

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    print 'pudge: Соединение c БД установлено.'
    cur = conn.cursor()
    conn.autocommit = True
    data = datetime.datetime.now()
    http = json.dumps(http)
    html = html
    source = json.dumps(source)
    durls_processed = durls_processed
    # Запросы
    #for i in range(len(durls_processed)):
    for item in durls_processed:
        cur.execute("SELECT id from pathes where domain=%s and path=%s", (url, item[0]))
        id = cur.fetchone()
        if id:
            cur.execute("INSERT INTO durls (path_id,args) VALUES (%s,%s)", (id[0],item[1]))
        else:
            cur.execute("INSERT INTO pathes (domain,path) VALUES (%s,%s)", (url,item[0]))
            #cur.execute("INSERT INTO durls (path_id,args) VALUES (%s,%s)", (id[0],item[1]))
        
        #cur.execute("INSERT INTO content (durl_id,http,html,sources,datetime) VALUES (%s,%s,%s,%s,%s)", (rows,http,html,sources,datetime))
        #cur.execute("INSERT INTO durls (path_id,args) VALUES (%s,%s)", (rows[0][0],item[1]))

        #cur.execute("SELECT id from pathes where path=%s", (durls_processed[i][0]))
        #rows = cur.fetchall()
        #if rows[0][0]:
        #    for row in rows:
        #        cur.execute("INSERT INTO durls (path_id,args) VALUES (%s,%s)", (row[0],durls_processed[i][0]))

    print 'pudge: Записано успешно.'
    conn.close()

def main(url, database, user, password, host, port):
    """
        Запуск всех частей программы.
    """

    http, html = make_request(url)
    source = get_source(html, url) # Ссылки на внешние файлы
    durls = get_durls(html, url) # Сырые ссылки навигации
    durls_processed = get_domain_durls(durls, url) #  Ссылки вида[(p, a), (p, a)..]
    #save_to_csv(http, html, durls_processed, source)
    #write_to_db(url,http, html, source, durls_processed, database, user, password, host, port)

if __name__ == '__main__':
    """
        Чтение конфига, получение домена из бд,
        чтение аргументов запуска.
    """

    parser = create_parser()
    args = parser.parse_args()
    default_url, database, user, password, host, port = get_config()
    if args.url:
        main(args.url, database, user, password, host, port)
    elif args.database == 1:
        domains = get_domain_from_database(database,user,password,host,port)
        # Передает первый домен из списка
        main(domains[0], database, user, password, host, port)
    else:
        main(default_url, database, user, password, host, port)