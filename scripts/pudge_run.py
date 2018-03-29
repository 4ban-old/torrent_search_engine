#!/usr/bin/python

import json
import Pudge
import sys


def _get_domains_config():
    import psycopg2

    db_user = 'pavel'
    db_name = 'comm'
    db_pass = 'pavel'
    db_host = 'localhost'
    conn = psycopg2.connect(database=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()
    cur.execute('select * from domains;')
    domains = cur.fetchall()
    domains_config = list()
    for domain in domains:
        try:
            sett = json.loads(domain[2])
        except ValueError:
            sett = {'config': {'string': 'domain=http://%s' % domain[1]}}
        if not sett:
            sett = {'config': {'string': 'domain=http://%s' % domain[1]}}
            # raise ValueError('No settings for domain %s - %s' % (domain[0], domain[1]))
        domains_config.append(sett['config']['string'])
    

    cur.close()
    conn.close()
    return domains_config

def _pudge_settings():
    sett = dict()
    sett['allow_subdomains'] = False
    sett['allow_parentdomains'] = False
    sett['allow_subpath'] = True
    sett['allow_parentpath'] = True
    sett['path_point'] = '/'
    sett['path_deep'] = 0
    sett['make_tree'] = True
    sett['save_http'] = True
    sett['save_html'] = True
    sett['save_durls'] = True
    sett['mode'] = 'chop-chop'
    sett['timewait'] = 2000
    # sett['user_agent'] = 'Mozilla/5.0 (compatible; komunist_bot/0.1; +http://komunist.ru/help/bots)'
    sett['domains'] = list()
    
    db = dict()
    db['host'] = 'localhost'
    db['name'] = 'comm'
    db['user'] = 'pavel'
    db['password'] = 'pavel'
    
    sett['db'] = db
    return sett

def main():
    config = _pudge_settings()
    if len(sys.argv)-1:
        url = sys.argv[1]
        config['domains'] = ["domain=%s" % url]
    else:
        config['domains'] = _get_domains_config()
    Pudge.run(config_dict=config)

if __name__ == '__main__':
    main()
