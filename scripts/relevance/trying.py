# coding: utf-8

import os
import psycopg2
import porter

from datetime import datetime

dict_size = 0

def get_dict():
    global dict_size
    home = os.environ['HOME']
    dictionary = os.path.join(home, 'dict.txt')
    dict_size = os.path.getsize(dictionary)
    f = open(dictionary, 'rb')
    return f


def get_line():

    f = get_dict()
    for line in f:
        line_size = len(line)
        yield line, line_size
    f.close()


def get_block():
    block = {}
    parent = ''
    roots = []
    p = porter.Porter()
    size = 0
    for line, line_size in get_line():
        size += line_size
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        if '|' in line:
            if line[0] == ' ':
                pass
            else:
                parent = line.partition('|')[0]
                parent = parent.strip()
                block[parent] = []

            line = line.split('|')
            line = map(lambda x: x.strip(), line)
            #line[0] = line[0].strip('*')
            root = p.get(unicode(line[0], 'utf-8'))
            roots.append(root)
            line.insert(1, root)
            block[parent].append(line)

        else:
            if block:
                block['roots'] = roots
                yield block, size
                block = {}
                parent = ''
                roots = []
                size = 0

def show_block(block):
    block = block.copy()
    roots = block.pop('roots')
    for key in block.keys():
        print key, ':::::'
        for item in block[key]:
            print '[',
            for i in item:
                print i, '|',
            print ']'


def check_roots(block):
    root = ''
    for key in block.keys():
        for item in block[key]:
            if not root:
                root = item[1]
            if root != item[1]:
                return 'Oops'

def set_connection():
    dbuser = 'pavel'
    dbname = 'dict'
    dbhost = 'localhost'
    dbpass = 'pavel'
    dbstring = "dbname='{dbname}' user='{dbuser}' host='{dbhost}' password='{dbpass}'"

    dbstring = dbstring.format(dbname=dbname, dbuser=dbuser, dbhost=dbhost, dbpass=dbpass)
    conn = psycopg2.connect(dbstring)
    #conn.autocommit = True
    return conn

def write_db_block(block, cur):
    """
        Writing dictionary into postgresql
    """
    query_in = "INSERT INTO \"{table}\" ({kinds}{pre_kind}) VALUES ({kinds_val}{pre_kind_val});"
    query_get = "SELECT {column} FROM {table} WHERE {kind}='{value}';"
    query = ''
    first = False
    group_id, root = '', ''
    roots = block.pop('roots')
    for key in block.keys():
        for val in block[key]:
            if not first:
                # at first we must find or create group
                first = True
                for root in roots:
                    # is there any of roots in database?
                    # if so, get group_id of this root
                    query = query_get.format(column='group_id', table='roots',
                                             kind='root', value=root)
                    cur.execute(query)
                    group_id = cur.fetchone()
                    if group_id is not None:
                        # we found it
                        break
                if group_id is None:
                    # there is no such roots,
                    # that mean there is no such group
                    root = val[1]
                    query = query_in.format(table='groups', kinds='\"group\"',
                                            pre_kind='', kinds_val='\'%s\'' % root, pre_kind_val='')
                    cur.execute(query)
                    cur.execute('SELECT LASTVAL()')
                    group_id = cur.fetchone()[0]
                else:
                    # get "id"
                    group_id = group_id[0]
            root = val[1]
            query = query_get.format(column='group_id', table='roots', kind='root', value=root)
            cur.execute(query)
            root = cur.fetchone()
            if root is None:
                # new root
                query = query_in.format(table='roots', kinds='\"root\"', pre_kind=', \"group_id\"',
                                        kinds_val='\'%s\'' % (val[1]),
                                        pre_kind_val=', \'%s\'' % (group_id))
                cur.execute(query)
            query = query_in.format(table='words', kinds='\"word\", \"specific\", \"num\"',
                                    pre_kind=', \"root\"',
                                    kinds_val='\'%s\', \'%s\', \'%s\'' % (val[0], val[2], val[3]),
                                    pre_kind_val=', \'%s\'' % (val[1]))
            cur.execute(query)


def block_to_list(block):
    res = []
    for key in block:
        for item in block[key]:
            res.append(item)
    return res

raw_word_id = 0
raw_block_id = 0
def write_raw_words(block, cur):
    global raw_word_id
    global raw_block_id
    query_word = "INSERT INTO raw_words (\"id\", \"word\", \"parent_word_id\", " \
                            "\"block_id\", \"root\", \"specific\", \"num\") " \
                 "VALUES (%s, %s, %s, %s, %s, %s, %s);"

    query_block = "INSERT INTO raw_blocks (\"id\") VALUES ('%s');"
    raw_block_id += 1
    cur.execute(query_block, (raw_block_id,))
    block.pop('roots')
    for key in block:
        for num, item in enumerate(block[key]):
            raw_word_id += 1
            if not num:
                raw_parent_word_id = raw_word_id
            cur.execute(query_word, (raw_word_id, item[0], raw_parent_word_id,
                                    raw_block_id, item[1], item[2], item[3],)
                        )


if __name__ == '__main__':

    word_count_commit = 0

    cur_times = []

    start_time = datetime.now()
    last_mess_time = start_time
    g = get_block()
    conn = set_connection()
    cur = conn.cursor()
    size = 0
    f_count = 2

    print "Started: %s" % start_time.ctime()
    print "..."
    while True:
        try:
            block, block_size = g.next()
            size += block_size
            if float(size)/float(dict_size)*100.0 > f_count:
                '''
                cur.execute('SELECT COUNT(*) FROM words;')
                words = cur.fetchone()[0]
                cur.execute('SELECT COUNT(*) FROM roots;')
                roots = cur.fetchone()[0]
                cur.execute('SELECT COUNT(*) FROM groups;')
                groups = cur.fetchone()[0]
                '''
                now_time = datetime.now()
                print "Readed %s%%, for %s from start, %s from last message" % (f_count, now_time - start_time, now_time - last_mess_time)
                # print "Got %s words, %s roots, %s groups" % (words, roots, groups)
                print 'Queries by 5000 words: max=%s, min=%s' % (max(cur_times), min(cur_times))
                f_count += 2
                last_mess_time = now_time
        except StopIteration:
            break

        # write_db_block(block, cur)
        write_raw_words(block, cur)
        word_count_commit += raw_word_id - word_count_commit
        if word_count_commit > 5000:
            start_cur_time = datetime.now()
            conn.commit()
            end_cur_time = datetime.now()
            cur_times.append(end_cur_time-start_cur_time)
            word_count_commit = 0


    now_time = datetime.now()
    print "Readed 100%%, for %s from start, %s from last message" % (now_time - start_time, now_time - last_mess_time)
    cur.close()
    conn.close()
